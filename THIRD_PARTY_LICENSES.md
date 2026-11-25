# Third-Party Licenses & Open-Source Attributions

This project is an unofficial open-source BYOA (Bring Your Own Assets) compatibility
engine built for Ren'Py 8. All third-party open-source components bundled or used at
build/runtime are listed below.

## 1. Bundled Open-Source Fonts (`Tsukihime_HD/game/fonts/`)

Full verbatim license texts are bundled directly in
`Tsukihime_HD/game/fonts/LICENSES.txt`.

| File | Font Family | Upstream Project | License |
|---|---|---|---|
| `lxgw_xihei.ttf` | LXGW Neo XiHei Plus v1.309 | https://github.com/lxgw/LxgwNeoXiHei | IPA Font License Agreement v1.0 |
| `lxgw_xihei_screen.ttf` | LXGW Neo XiHei Screen Full | https://github.com/lxgw/LxgwNeoXiZhi-Screen | IPA Font License Agreement v1.0 |
| `notoserif_sc.otf` | Noto Serif SC Regular | https://github.com/notofonts/noto-cjk | SIL Open Font License 1.1 |
| `lxgw_wenkai.ttf` | LXGW WenKai Lite v1.530 | https://github.com/lxgw/LxgwWenKai-Lite | SIL Open Font License 1.1 |
| `notosans_med.otf` | Noto Sans SC Medium | https://github.com/notofonts/noto-cjk | SIL Open Font License 1.1 |
| `lora_reg.ttf`, `lora_italic.ttf` | Lora Regular & Italic | https://github.com/cyrealtype/Lora-Cyrillic | SIL Open Font License 1.1 |

## 2. Runtime Engine (User-Provided / Release Package)

- **Ren'Py Visual Novel Engine** (`renpy-8.5.3-sdk`): MIT License (plus bundled
  LGPL 2.1 / zlib / FreeType / libpng / libwebp / FFmpeg libraries as documented
  in Ren'Py's `LICENSE.txt`). Not committed to Git; downloaded separately or
  packaged in binary releases with Ren'Py's full `LICENSE.txt`.

## 3. Optional Local HD Upscaler (Not Bundled in Git)

- **Real-ESRGAN ncnn Vulkan** (`realesrgan-ncnn-vulkan` & `realesrgan-x4plus-anime`):
  BSD-3-Clause License (https://github.com/xinntao/Real-ESRGAN). Optional tool
  for `--quality hd` local upscaling only.

## 4. Python Build Dependencies (Local Import Only)

- **Pillow (PIL)**: HPND / MIT-CMU License
- **NumPy**: BSD-3-Clause License
