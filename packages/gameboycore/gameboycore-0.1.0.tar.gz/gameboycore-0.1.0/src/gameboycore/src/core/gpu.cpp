#include "gameboycore/gpu.h"
#include "gameboycore/palette.h"
#include "gameboycore/memorymap.h"
#include "gameboycore/pixel.h"
#include "gameboycore/interrupt_provider.h"
#include "gameboycore/tilemap.h"

#include "bitutil.h"

namespace gb
{
	static constexpr auto HBLANK_CYCLES = 207;
	static constexpr auto VBLANK_CYCLES = 4560;
	static constexpr auto OAM_ACCESS_CYCLES = 83;
	static constexpr auto LCD_TRANSFER_CYCLES = 175;

	static constexpr auto LINE_CYCLES = 456;
	static constexpr auto VBLANK_LINE = 144;
	static constexpr auto LINE_MAX = 153;

	/* Private Implementation */

	class GPU::Impl
	{
	public:
		enum class Mode
		{
			HBLANK,
			VBLANK,
			OAM,
			LCD
		};

		Impl(MMU::Ptr& mmu) :
			mmu_(mmu),
			mode_(Mode::OAM),
			cycle_count_(0),
			line_(0),
			lcdc_(mmu->get(memorymap::LCDC_REGISTER)),
			stat_(mmu->get(memorymap::LCD_STAT_REGISTER)),
			vblank_provider_(*mmu.get(), InterruptProvider::Interrupt::VBLANK),
			stat_provider_(*mmu.get(), InterruptProvider::Interrupt::LCDSTAT)
		{
			mmu->addWriteHandler(memorymap::LCDC_REGISTER, std::bind(&Impl::configure, this, std::placeholders::_1, std::placeholders::_2));
		}

		void update(uint8_t cycles, bool ime)
		{
			if (IS_CLR(lcdc_, memorymap::LCDC::ENABLE)) return; // FIXME: some games don't with this enabled!

			cycle_count_ += cycles;

			switch (mode_)
			{
				case Mode::HBLANK:
					// check if the HBLANK period is over
					if (hasElapsed(HBLANK_CYCLES))
					{
						// render the current scan line
						renderScanline();
						// update the scan line
						updateLY();
						// check if LY matches LYC
						compareLyToLyc(ime);

						// check if in VBlank mode
						if (line_ == VBLANK_LINE)
						{
							mode_ = Mode::VBLANK;
							vblank_provider_.set();
						}
						else
						{
							mode_ = Mode::OAM;
						}

						checkStatInterrupts(ime);
					}
					break;
				case Mode::OAM:
					if (hasElapsed(OAM_ACCESS_CYCLES))
					{
						mode_ = Mode::LCD;
					}
					break;
				case Mode::LCD:
					if (hasElapsed(LCD_TRANSFER_CYCLES))
					{
						mode_ = Mode::HBLANK;
						checkStatInterrupts(ime);
					}
					break;
				case Mode::VBLANK:
					if (hasElapsed(LINE_CYCLES))
					{
						updateLY();
						compareLyToLyc(ime);

						if (line_ == 0)
						{
							mode_ = Mode::OAM;
							checkStatInterrupts(ime);
						}
					}
					break;
			}

		}

		void setRenderCallback(RenderScanlineCallback callback)
		{
			render_scanline_ = callback;
		}

	private:

		void renderScanline()
		{
			Scanline scanline;
			std::array<uint8_t, 160> color_line;
			TileMap tilemap(*mmu_.get());

			auto background_palette = Palette::get(mmu_->read(memorymap::BGP_REGISTER));

			// get lcd config
			const auto lcdc = mmu_->read(memorymap::LCDC_REGISTER);

			const auto background_enabled = IS_SET(lcdc, memorymap::LCDC::BG_DISPLAY_ON) != 0;
			const auto window_enabled     = IS_SET(lcdc, memorymap::LCDC::WINDOW_ON)     != 0;
			const auto sprites_enabled    = IS_SET(lcdc, memorymap::LCDC::OBJ_ON)        != 0;

			// get background tile line
			const auto background = tilemap.getBackground(line_);

			// get window overlay tile line
			const auto window = tilemap.getWindowOverlay(line_);
			const auto wx = mmu_->read(memorymap::WX_REGISTER);
			const auto wy = mmu_->read(memorymap::WY_REGISTER);

			// compute a scan line
			for (auto pixel_idx = 0u; pixel_idx < scanline.size(); ++pixel_idx)
			{
				auto color = 0u;

				if (window_enabled && line_ >= (int)wy && (int)pixel_idx >= (wx - 7))
					color = window[pixel_idx];
				else if (background_enabled)
					color = background[pixel_idx];
				else
					color = 0;

				color_line[pixel_idx] = color;
				scanline[pixel_idx] = background_palette[color];
			}

			if (sprites_enabled)
				tilemap.drawSprites(scanline, color_line, line_);

			// send scan line to the renderer
			if (render_scanline_ && line_ < VBLANK_LINE)
				render_scanline_(scanline, line_);
		}

		bool hasElapsed(int mode_cycles)
		{
			if (cycle_count_ >= mode_cycles)
			{
				cycle_count_ -= mode_cycles;
				return true;
			}
			return false;
		}

		void updateLY()
		{
			line_ = (line_ + 1) % LINE_MAX;
			mmu_->write((uint8_t)line_, memorymap::LY_REGISTER);
		}

		void configure(uint8_t value, uint16_t addr)
		{
			bool enable = (value & memorymap::LCDC::ENABLE) != 0;

			if (enable && IS_CLR(lcdc_, memorymap::LCDC::ENABLE))
			{
				line_ = 0;
				cycle_count_ = 0;
			}

			lcdc_ = value;
		}

		void compareLyToLyc(bool ime)
		{
			auto lyc = mmu_->read(memorymap::LYC_REGISTER);

			if ((uint8_t)line_ == lyc)
			{
				//stat_ |= memorymap::Stat::LYCLY;
				SET(stat_, memorymap::Stat::LYCLY);
			}
			else
			{
				//stat_ &= ~(memorymap::Stat::LYCLY);
				CLR(stat_, memorymap::Stat::LYCLY);
			}

			// check the ly=lyc flag
			if (stat_ & memorymap::Stat::LYCLY)
			{
				if (ime)
					stat_provider_.set();
			}
		}

		void checkStatInterrupts(bool ime)
		{
		//	InterruptProvider stat_provider{ *mmu_.get(), InterruptProvider::Interrupt::LCDSTAT };

			// check mode selection interrupts
			uint8_t mask = (1 << (3 + static_cast<uint8_t>(mode_)));

			if (stat_ & mask)
			{
				if (ime)
					stat_provider_.set();
			}
		}

	private:
		MMU::Ptr& mmu_;

		Mode mode_;
		int cycle_count_;
		int line_;
		uint8_t& lcdc_;
		uint8_t& stat_;

		InterruptProvider vblank_provider_;
		InterruptProvider stat_provider_;

		RenderScanlineCallback render_scanline_;
	};

	/* Public Implementation */

	GPU::GPU(MMU::Ptr& mmu) :
		impl_(new Impl(mmu))
	{
	}

	GPU::~GPU()
	{
		delete impl_;
	}

	void GPU::update(uint8_t cycles, bool ime)
	{
		impl_->update(cycles, ime);
	}

	void GPU::setRenderCallback(RenderScanlineCallback callback)
	{
		impl_->setRenderCallback(callback);
	}

} // namespace gb
