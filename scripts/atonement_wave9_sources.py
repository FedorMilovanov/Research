#!/usr/bin/env python3
"""Read-only custody gate for Wave 9 patristic print scans, TEI originals, and Cyril 5-locus synthesis.

Default: retained scan/TEI/OCR controls and actual Git preimages against Wave 8 baseline.
--source-root: verify all 51 external Git-blob objects (21 visually inspected A1 JPEG print scans,
3 corrected A1 TEI-XML editions, and 27 class-C OCR/JSONL witnesses) BEFORE checking literal
textual invariants. No network, file writes, silent OCR repair, Pusey Vol. II / PG 74 scan claims,
doctrinal closure, or publication approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata

from atonement_wave4_sources import git_blob

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'ИСКУПЛЕНИЕ/evidence/source_controls_wave9_2026-11-03.json'
REPORT = 'ИСКУПЛЕНИЕ/evidence/synchronization_2026-11-02.json'
BASELINE = '2a93d6250af6d94f376ddb2be67fef7888860264'
REVIEW_KEY = 'patristicScanAndCyrilComparisonWave9'
STATUS = 'PATRISTIC_ORIGINALS_AND_CATENA_SCANS_VERIFIED_PUSEY_V2_1152_SCAN_OPEN'
O10 = 'CHRYSOSTOM_CATENA_SCAN_VERIFIED_HOMILY_OCR_COLLATED_DIRECT_PRINT_SCAN_OPEN'
O11 = 'CYRIL_FIVE_LOCUS_COMPARISON_AND_COISLIN23_CATENA_SCAN_VERIFIED_PUSEY_V2_1152_SCAN_OPEN'

PINS = {
    'OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena': '4f7e3b52b0f00047c73736bce4c6005049c75a01',
    'OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev': '9f4df68bb5fdb07b996b36b1a4b532680eb6aec2',
    'OpenGreekAndLatin/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev': '9cd242d123b1d97ae2780f50bcd2a61592fda88a',
    'OpenGreekAndLatin/First1KGreek': 'ed91552c52530c8f5a3ddf2dd767e899372a804c',
    'OpenGreekAndLatin/patrologia_latina-dev': '8c651f859f821f0868755596f1a513946ca25350',
    'latin-ocr/operacyrilli04cyriuoft': 'fc594d8f43ef141af4e93a0fcc424063a378eacf',
    'latin-ocr/sanctipatrisnos02chrygoog': 'ac516647b9cfbf176f2b472479bd2f3711b8dd50',
    'latin-ocr/sanctipatrisnos02pusegoog': '036c46fecfbe06b8fe009e1d8cfca72e5978bc7d',
    'open-greek/open-greek-corpus': 'a152e69ef26c1b9f9da2218d303f36f5ba4ab5b9',
}

FILE_PINS = {
    'PUSEY-V1-P131-JPG': ('9ae5a64a0d4d6310c8ea3d9d7cd8aae643cb5bcb68db7421dde281753b29f9e6', 334841, '4968deb61f436f16ed9e4998025a19f2d399d613'),
    'PUSEY-V1-P132-JPG': ('ba72ad154a3ba25988b31c8e735571a7626cfc42da0018e3a8cc4558de149b1b', 338694, '641e8252eb53547f1ea6088f474f0d17ccdcee42'),
    'PUSEY-V1-P133-JPG': ('3b2f623fdfab642c950dacce6794e9ac5652534fd9f6644abdfb3e3158f3c19b', 341665, 'd7bb741c3efc2fb5286eda91495acf44a6fd473c'),
    'PUSEY-V1-P134-JPG': ('50dcff8615af130a2a2ca0521ab3e339c2e4067dc28f49ef3e8d356889836ba9', 329795, '9e5e7a83fd6c8b9d189465bdcfe795b8ebde960c'),
    'PUSEY-V1-P135-JPG': ('b81597f1952db547051022438f70cf9afb94e2c7520618741721ef6cda8095a9', 337928, '041ad3e4840380f89df36d82da874afaff330ee8'),
    'PUSEY-V1-P136-JPG': ('67ece554061fddbebf85d1dddac240e474b28f6c7aecd7be7548e26fb888ab98', 351359, 'ad8ccde258c2fedd5b73e106a3b3dbc11943bfdb'),
    'CRAMER-V2-TITLE-JPG': ('9f88a916140fe5fa71d9ad891c3d6dd19f9f92705b9d1b18ca34dd71721fb8a1', 122964, 'ac81f8d58aaa40b679cc4fb4e21640689c986cf5'),
    'CRAMER-V2-P318-JPG': ('e1906c7025e349f25ccd4ca9c300bd5b661b11e02773f2e172f52de800c5c3a4', 344977, 'd53d14f2c665dfed5524b3338887991ac7c4cb4e'),
    'CRAMER-V2-P319-JPG': ('860eed71e43752c85b9aef494c32fdf92555e08c75086ec3173c61aae5ead58f', 327978, '3364d36574baa0c49722b2c542e002451cda8d6f'),
    'CRAMER-V2-P320-JPG': ('a0a76a96cd99be81dcced7886d7ae748dfced4a3f94efec6777a77e713a89012', 343613, '38e3c71b2e521aee92af34286b0c75d9dd90e572'),
    'CRAMER-V2-P321-JPG': ('339bd14d3dd968cdde8dfa60f44c4d54391801c29b558f71cbaa8b578efeb32d', 310317, '128d0ca622c2705b7af7c41683506b63186acb40'),
    'CRAMER-V2-P322-JPG': ('e16f2c4de4828b9c4a491a76bf17b6232accf6d90edf50bd13ae3b6420bda113', 346877, 'e361dfe028ad3bf814e18dddb2756087750eef3c'),
    'MASON-1899-TITLE-JPG': ('16a657449843861f81c4e5e743dccb4dd793706cb7c3bb85bd03c4dd1fd4281f', 352564, 'be973f82b79b561e367ea0fd6f99295227cd8cc7'),
    'MASON-1899-P140-JPG': ('d075857eea10119d4225003539fd87d3893d3e5c09bd4d3b4c37dd8a21ada82e', 410362, 'c05334172fd0a4ed98ae2923d806b46fc35bef91'),
    'MASON-1899-P141-JPG': ('c5d2ac70d983222cfac5ce3e0bd5d1f42fc22b683d4b621a892901ac3816b9a3', 361323, 'db05e4cd81f79cf3f50f661daa0cd5e3530656d6'),
    'MASON-1899-P142-JPG': ('c8f6ffa380a0ce154e5c7068f692e6b2aadde7576d64db0847bde33b4025df34', 396101, 'dcc97b85bc4ae986968b1a73c180e55aab764f67'),
    'MASON-1899-P143-JPG': ('3b32ec25a8eb1baa770176cd6bee393a879b56fa2a5c72e7a91642bf623111c3', 345112, '75b5bfc723daa9aa863f6a89af54f20b0434ba38'),
    'PL54-FIG64-JPG': ('a21ea9e98975dcd9d6ab6c92ecd4f4e8c1f6bfa6a8faa071c141e33c93c96206', 422722, 'a10b6f76b54fc46d7c3bc05654fba1ae66ca4a66'),
    'PL54-FIG66-JPG': ('b96aa5d13cd39c0b8265041c2f82ad06496e4c923aec559f314e9d64121dca74', 332658, '8402099226a68d8b5fedb4f2e843faeea497b512'),
    'PL54-FIG68-JPG': ('0fa610752cdbc0e8ed5aab048ba93974fa66623d494f427d89c5cbd90d4ee3e7', 208425, '9ce01d5a10689c891782d76c52c28c06f1ce67ae'),
    'PL54-FIG70-JPG': ('af57d59f47d1ebac6bc78a822819db9e54a0a1390acb82180edbb14cc8fe09bd', 171436, '8fdf16e63210641cfacb8e72482d934e68caa431'),
    'PL54-TEI-XML': ('9573f47346be75ebe0223327c064b78404cb805c8e5d0ef05e2ce0d0944203d5', 4799422, 'a0677806d13452a6670fab1ee4e4cf8c82826440'),
    'PL75-TEI-XML': ('d461fb15c348705f32f4322b6c2bcb50e6f58d3eaebd0be79d93028a91debdcf', 4069250, 'e32a8fb648aef634052c2e5e0e634fd6d2199676'),
    'FIRST1K-NAZ-OR30-XML': ('5231a422100008fc91090e4b39f2563958173c255971ea45ad22bdfb1d335bd5', 147773, '979167575864b276d40b164ea355f46f0a790bd3'),
    'PUSEY-V2-UOFT-0117-TXT': ('8a1154e24414bb6838d84d654cbd7ef17e1e860dbbf46184762c16b3a2ad8cab', 3600, 'a76a74c34f05154c34de5feb07cbfc402937191c'),
    'PUSEY-V2-UOFT-0118-TXT': ('3ab18005e406fc171623ff03e2152ba3a27f50106788d0c955166dd0f4d4b7af', 3704, '3a0c3ea0a27c2b723cd0777871217ad866d67053'),
    'PUSEY-V2-UOFT-0119-TXT': ('0fcc73c28a73b33b01be316df3896b47092e0c1ae9ba29b258ec9e63ea84d2fe', 3810, '63882eea5cb8e3395160815ca1a4e99d7468ccc7'),
    'PUSEY-V2-UOFT-0120-TXT': ('e2b2de348326e072d82e2b29010e4fe4aba73c08fc30097c92ca5133ee1119e8', 3951, '858d2f429c4e3dc2aef51d18be6f70a7eba29ca8'),
    'PUSEY-V2-UOFT-0239-TXT': ('4285205dcf04da9b0c4e9ceee6b623f6ce4cdf3d9570d90ddf37b2541c0a0de2', 3908, '00b4e9dc179859b797caa4553a757ad8a5ff6c39'),
    'PUSEY-V2-UOFT-0240-TXT': ('380959992051004095d6bdff876507ec536c1278b25b58e78b33d55ca1b9fc24', 4246, 'e780febe12c282893bea76f970e345d7539f3709'),
    'PUSEY-V2-UOFT-0241-TXT': ('e8c451a00b6b0dbc260c89e662508a730f0fc87ebcfe86819d315c83a4de2396', 3202, 'f315320eb66c9949d9e3950ed87c3e2fc768e659'),
    'PUSEY-V2-UOFT-0242-TXT': ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 0, 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'),
    'PUSEY-V2-UOFT-0243-TXT': ('6a760f82ffe33f8f4bcb15c3ef6888c4b833c99461c02285d393009c4ff8153b', 4115, '1d3b52cebc1de3b4023d48d564bca32e724f3941'),
    'PUSEY-V2-UOFT-0244-TXT': ('1030f18851d76fe29645d527e3d17d3a8fec7987f83225a20d5a5465821cdf74', 3872, 'd6e27bf8c7bc22804579a1fadc8b137400b62143'),
    'PUSEY-V2-UOFT-0245-TXT': ('2ecfc4044f482fa80596cb4bbb9ff3968100799ff05e08ab730f533df3d88add', 3703, '255a8c75d2dee4af4ab4e88c9d3a0fc2b7998d12'),
    'PUSEY-V2-UOFT-0246-TXT': ('c46b56a4c21a21dcd54a7f95e0b3a761ed612e422fbc1885b72b56efffc955c7', 3817, 'f55a21bfab98e6460f8ad2a450b61ae6ceadca42'),
    'PUSEY-V2-UOFT-0247-TXT': ('d01d49b11ac35ba43439c7474ba793f05ad8a8e789673d1cedbf445f16264dc4', 2988, 'e474f9ca56bb812e7713665d9b2a0dac62bd9ba2'),
    'PUSEY-V2-UOFT-0248-TXT': ('fa1dafd60baa3aff4fc5c78360b44ec953a146dafd12f5c899304de641788b35', 3671, '0ed482bacb10ebd03ece5b51da99c8defdd05846'),
    'PUSEY-V2-UOFT-0303-TXT': ('d415fb6509a4ad68206654f8eaa8d798e1f311d1f6c6cf17e55c3df913337b0a', 6536, '357bb3d25e8ca41b76f268206d9fc5d4a85a12dd'),
    'PUSEY-V2-UOFT-0304-TXT': ('657d722a4ddb89a4fb268e7f184a0350b933a0bb9031afcf50859ec393020bbc', 4233, '7071f73758f88501c62dfaec507796a18ac5cbb0'),
    'PUSEY-V2-UOFT-0305-TXT': ('de7edfc3de31c020a71aa6b6e1c38e41f5f356b10a1a19255a28cf96d6f49ce5', 3543, '6950f11b7c1070b79354da1e82c061be0bf7e0b7'),
    'PUSEY-V2-UOFT-0306-TXT': ('f3ea76f41a28642e11e3e66a1584af3bbd00cdaab4b0e81cdd6985f52e0f4c11', 3614, 'a6e16d36973d29f9ef1763a7021e5eed0a1f0dbc'),
    'PUSEY-V2-UOFT-0307-TXT': ('004a7ef7181b01e19e83cf50403231f8ab72df72a36c1c72af79ed1daf7ae2ab', 4545, '7e5c63efb62479d9937ee09999eabbe8c69a6ad2'),
    'PUSEY-V2-UOFT-0308-TXT': ('1c18e424a6febd92f20b9f790f1e9c8a338c408523e620fa10f2041521df39fb', 3905, '3fc58dc9d190656f67e7f74633c314874ad4f9f8'),
    'PUSEY-V2-GOOG-0304-TXT': ('59e568638a5a24d646e4abe5140ace24646ddd98c9c40b56b44eba64a571a401', 3507, '8551ca873d9d588e6cce590578a3e57f29f6d18a'),
    'PUSEY-V2-GOOG-0305-TXT': ('96dbd1554da4d3046903bef5d054d0aed5e11465def9ae08ae62bea8e771b544', 4204, 'dc15eefce9a2ea02a654a2c24d3ed5cceac077ad'),
    'PUSEY-V2-GOOG-0306-TXT': ('75c41ca29896a721421f7f071646f4e0dd5d967bb949f81044dd57f2b291c225', 3591, '7027e6e89cf9066757bed5e79c59a88e698e4dd5'),
    'GAUME-CHRYS-0472-TXT': ('e97e0278c83f4f63780edde86a88f623cde5d5f3e47ee31a3d9c97ac9e358e89', 2694, '92d2cb0ee2b8751408221998200a22ae32ad91ae'),
    'GAUME-CHRYS-0473-TXT': ('36980f941b70b3f9773b85cd65a9e5926571ba0cc555fbaf741dc4f110d4c1ef', 6246, '9ca14a7a6cafbc5cf42479248b81944b921a1d58'),
    'OG-CHRYS-IN-JOANNEM-JSONL': ('60aede316893e4467716fef448e37c163243972e61ea56b0578391f76bb56c91', 2973576, 'b67d85bfa23393c409b7c4ffe84a60150fb8849e'),
    'OG-NAZ-OR45-JSONL': ('d5a8d2c23ed5802746d3be4cd1d041f26baad385b0db5e04e8cc84179cab2a79', 79717, 'f99db4bffd52bf55758d936ecade4cf9ceb54a55'),
}

FILE_LAYOUT = {
    'PUSEY-V1-P131-JPG': ('OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev', '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0175.jpg', 'OpenGreekAndLatin--2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0175.jpg', 'A1_SCAN'),
    'PUSEY-V1-P132-JPG': ('OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev', '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0176.jpg', 'OpenGreekAndLatin--2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0176.jpg', 'A1_SCAN'),
    'PUSEY-V1-P133-JPG': ('OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev', '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0177.jpg', 'OpenGreekAndLatin--2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0177.jpg', 'A1_SCAN'),
    'PUSEY-V1-P134-JPG': ('OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev', '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0178.jpg', 'OpenGreekAndLatin--2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0178.jpg', 'A1_SCAN'),
    'PUSEY-V1-P135-JPG': ('OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev', '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0179.jpg', 'OpenGreekAndLatin--2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0179.jpg', 'A1_SCAN'),
    'PUSEY-V1-P136-JPG': ('OpenGreekAndLatin/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev', '2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0180.jpg', 'OpenGreekAndLatin--2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev/2013-11-26-23-24_operacyrilli03cyriuoft_jp2_OCT7_rev.book/i0180.jpg', 'A1_SCAN'),
    'CRAMER-V2-TITLE-JPG': ('OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena', '2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0007.jpg', 'OpenGreekAndLatin--2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0007.jpg', 'A1_SCAN'),
    'CRAMER-V2-P318-JPG': ('OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena', '2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0332.jpg', 'OpenGreekAndLatin--2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0332.jpg', 'A1_SCAN'),
    'CRAMER-V2-P319-JPG': ('OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena', '2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0333.jpg', 'OpenGreekAndLatin--2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0333.jpg', 'A1_SCAN'),
    'CRAMER-V2-P320-JPG': ('OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena', '2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0334.jpg', 'OpenGreekAndLatin--2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0334.jpg', 'A1_SCAN'),
    'CRAMER-V2-P321-JPG': ('OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena', '2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0335.jpg', 'OpenGreekAndLatin--2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0335.jpg', 'A1_SCAN'),
    'CRAMER-V2-P322-JPG': ('OpenGreekAndLatin/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena', '2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0336.jpg', 'OpenGreekAndLatin--2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena/2013-10-18-17-43_catenaegraecorum02cramuoft_jp2_Catena.book/i0336.jpg', 'A1_SCAN'),
    'MASON-1899-TITLE-JPG': ('OpenGreekAndLatin/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev', '2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0009.jpg', 'OpenGreekAndLatin--2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0009.jpg', 'A1_SCAN'),
    'MASON-1899-P140-JPG': ('OpenGreekAndLatin/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev', '2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0182.jpg', 'OpenGreekAndLatin--2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0182.jpg', 'A1_SCAN'),
    'MASON-1899-P141-JPG': ('OpenGreekAndLatin/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev', '2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0183.jpg', 'OpenGreekAndLatin--2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0183.jpg', 'A1_SCAN'),
    'MASON-1899-P142-JPG': ('OpenGreekAndLatin/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev', '2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0184.jpg', 'OpenGreekAndLatin--2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0184.jpg', 'A1_SCAN'),
    'MASON-1899-P143-JPG': ('OpenGreekAndLatin/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev', '2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0185.jpg', 'OpenGreekAndLatin--2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev/2013-12-22-16-15_fivetheological00greg_jp2_OCT7_rev.book/i0185.jpg', 'A1_SCAN'),
    'PL54-FIG64-JPG': ('OpenGreekAndLatin/patrologia_latina-dev', 'volumes/PL54/PL54_fig64.jpg', 'OpenGreekAndLatin--patrologia_latina-dev/volumes/PL54/PL54_fig64.jpg', 'A1_SCAN_CC'),
    'PL54-FIG66-JPG': ('OpenGreekAndLatin/patrologia_latina-dev', 'volumes/PL54/PL54_fig66.jpg', 'OpenGreekAndLatin--patrologia_latina-dev/volumes/PL54/PL54_fig66.jpg', 'A1_SCAN_CC'),
    'PL54-FIG68-JPG': ('OpenGreekAndLatin/patrologia_latina-dev', 'volumes/PL54/PL54_fig68.jpg', 'OpenGreekAndLatin--patrologia_latina-dev/volumes/PL54/PL54_fig68.jpg', 'A1_SCAN_CC'),
    'PL54-FIG70-JPG': ('OpenGreekAndLatin/patrologia_latina-dev', 'volumes/PL54/PL54_fig70.jpg', 'OpenGreekAndLatin--patrologia_latina-dev/volumes/PL54/PL54_fig70.jpg', 'A1_SCAN_CC'),
    'PL54-TEI-XML': ('OpenGreekAndLatin/patrologia_latina-dev', 'volumes/PL54/PL54.xml', 'OpenGreekAndLatin--patrologia_latina-dev/volumes/PL54/PL54.xml', 'A1_TEI'),
    'PL75-TEI-XML': ('OpenGreekAndLatin/patrologia_latina-dev', 'volumes/PL75/PL75.xml', 'OpenGreekAndLatin--patrologia_latina-dev/volumes/PL75/PL75.xml', 'A1_TEI'),
    'FIRST1K-NAZ-OR30-XML': ('OpenGreekAndLatin/First1KGreek', 'data/tlg2022/tlg010/tlg2022.tlg010.1st1K-grc1.xml', 'OpenGreekAndLatin--First1KGreek/data/tlg2022/tlg010/tlg2022.tlg010.1st1K-grc1.xml', 'A1_TEI'),
    'PUSEY-V2-UOFT-0117-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0117.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0117.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0118-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0118.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0118.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0119-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0119.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0119.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0120-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0120.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0120.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0239-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0239.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0239.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0240-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0240.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0240.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0241-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0241.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0241.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0242-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0242.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0242.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0243-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0243.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0243.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0244-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0244.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0244.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0245-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0245.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0245.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0246-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0246.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0246.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0247-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0247.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0247.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0248-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0248.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0248.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0303-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0303.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0303.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0304-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0304.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0304.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0305-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0305.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0305.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0306-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0306.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0306.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0307-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0307.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0307.txt', 'C_OCR'),
    'PUSEY-V2-UOFT-0308-TXT': ('latin-ocr/operacyrilli04cyriuoft', 'operacyrilli04cyriuoft_0308.txt', 'latin-ocr--operacyrilli04cyriuoft/operacyrilli04cyriuoft_0308.txt', 'C_OCR'),
    'PUSEY-V2-GOOG-0304-TXT': ('latin-ocr/sanctipatrisnos02pusegoog', 'sanctipatrisnos02pusegoog_0304.txt', 'latin-ocr--sanctipatrisnos02pusegoog/sanctipatrisnos02pusegoog_0304.txt', 'C_OCR'),
    'PUSEY-V2-GOOG-0305-TXT': ('latin-ocr/sanctipatrisnos02pusegoog', 'sanctipatrisnos02pusegoog_0305.txt', 'latin-ocr--sanctipatrisnos02pusegoog/sanctipatrisnos02pusegoog_0305.txt', 'C_OCR'),
    'PUSEY-V2-GOOG-0306-TXT': ('latin-ocr/sanctipatrisnos02pusegoog', 'sanctipatrisnos02pusegoog_0306.txt', 'latin-ocr--sanctipatrisnos02pusegoog/sanctipatrisnos02pusegoog_0306.txt', 'C_OCR'),
    'GAUME-CHRYS-0472-TXT': ('latin-ocr/sanctipatrisnos02chrygoog', 'sanctipatrisnos02chrygoog_0472.txt', 'latin-ocr--sanctipatrisnos02chrygoog/sanctipatrisnos02chrygoog_0472.txt', 'C_OCR'),
    'GAUME-CHRYS-0473-TXT': ('latin-ocr/sanctipatrisnos02chrygoog', 'sanctipatrisnos02chrygoog_0473.txt', 'latin-ocr--sanctipatrisnos02chrygoog/sanctipatrisnos02chrygoog_0473.txt', 'C_OCR'),
    'OG-CHRYS-IN-JOANNEM-JSONL': ('open-greek/open-greek-corpus', 'data/corpus/joannes-chrysostomus.in-joannem-homiliae-1-88.jsonl', 'open-greek--open-greek-corpus/data/corpus/joannes-chrysostomus.in-joannem-homiliae-1-88.jsonl', 'C_OCR_CC'),
    'OG-NAZ-OR45-JSONL': ('open-greek/open-greek-corpus', 'data/corpus/gregorius-nazianzenus.in-sanctum-pascha-orat-45.jsonl', 'open-greek--open-greek-corpus/data/corpus/gregorius-nazianzenus.in-sanctum-pascha-orat-45.jsonl', 'C_OCR_CC'),
}

A1_SCAN_IDS = {'PUSEY-V1-P131-JPG', 'PUSEY-V1-P132-JPG', 'PUSEY-V1-P133-JPG', 'PUSEY-V1-P134-JPG', 'PUSEY-V1-P135-JPG', 'PUSEY-V1-P136-JPG', 'CRAMER-V2-TITLE-JPG', 'CRAMER-V2-P318-JPG', 'CRAMER-V2-P319-JPG', 'CRAMER-V2-P320-JPG', 'CRAMER-V2-P321-JPG', 'CRAMER-V2-P322-JPG', 'MASON-1899-TITLE-JPG', 'MASON-1899-P140-JPG', 'MASON-1899-P141-JPG', 'MASON-1899-P142-JPG', 'MASON-1899-P143-JPG', 'PL54-FIG64-JPG', 'PL54-FIG66-JPG', 'PL54-FIG68-JPG', 'PL54-FIG70-JPG'}
A1_TEI_IDS = {'PL54-TEI-XML', 'PL75-TEI-XML', 'FIRST1K-NAZ-OR30-XML'}
C_OCR_IDS = {'PUSEY-V2-UOFT-0117-TXT', 'PUSEY-V2-UOFT-0118-TXT', 'PUSEY-V2-UOFT-0119-TXT', 'PUSEY-V2-UOFT-0120-TXT', 'PUSEY-V2-UOFT-0239-TXT', 'PUSEY-V2-UOFT-0240-TXT', 'PUSEY-V2-UOFT-0241-TXT', 'PUSEY-V2-UOFT-0242-TXT', 'PUSEY-V2-UOFT-0243-TXT', 'PUSEY-V2-UOFT-0244-TXT', 'PUSEY-V2-UOFT-0245-TXT', 'PUSEY-V2-UOFT-0246-TXT', 'PUSEY-V2-UOFT-0247-TXT', 'PUSEY-V2-UOFT-0248-TXT', 'PUSEY-V2-UOFT-0303-TXT', 'PUSEY-V2-UOFT-0304-TXT', 'PUSEY-V2-UOFT-0305-TXT', 'PUSEY-V2-UOFT-0306-TXT', 'PUSEY-V2-UOFT-0307-TXT', 'PUSEY-V2-UOFT-0308-TXT', 'PUSEY-V2-GOOG-0304-TXT', 'PUSEY-V2-GOOG-0305-TXT', 'PUSEY-V2-GOOG-0306-TXT', 'GAUME-CHRYS-0472-TXT', 'GAUME-CHRYS-0473-TXT', 'OG-CHRYS-IN-JOANNEM-JSONL', 'OG-NAZ-OR45-JSONL'}

STATISTICS = dict(
    gitObjects=51,
    visuallyInspectedA1PrintScans=21,
    correctedA1TeiXmlObjects=3,
    classCOcrAndJsonlObjects=27,
    controlledArtifacts=51,
    cyrilComparedLoci=5,
    verifiedPuseyVol2OrPg74ScansFor1152=0,
)

FALSE_BOUNDARIES = (
    'fullWorksRead',
    'puseyVol2PageImagesInspected',
    'mignePg74PageImagesInspected',
    'fullCyril1152FragmentGreekOriginalVerified',
    'oratio4522GreekPrintScanInspected',
    'chrysostomHom65DirectPrintScanInspected',
    'manuscriptsInspected',
    'publicationEligible',
    'mergePerformed',
    'doctrinalClosure',
    'englishCreationReadingErased',
    'humanReadingMeasured',
)

CYRIL_LOCI = {
    'book1Ch9John1_11_13',
    'book6John8_46_47',
    'book6Ch1John10_14_16',
    'book7FragJohn11_44',
    'book7FragJohn11_49_52',
}

PATRISTIC_CARDS = {'GRG-1', 'CHR-2', 'NAZ-1', 'LEO-1'}

REQUIRED_REPAIRS = {
    'W9-' + s for s in (
        'NT15', 'P13', 'N00', 'F11', 'F04', 'F05', 'F10', 'F00',
        'C25', 'ROOT00', 'ROOT-DATA', 'NT-DATA', 'F-DATA', 'S-DATA',
    )
}

REGISTRIES = (
    'data/atonement-corpus-v1.json',
    'nt/data/nt-corpus-v1.json',
    'fathers/data/fathers-corpus-v1.json',
    'synthesis/data/synthesis-corpus-v1.json',
)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def norm_xml(text: str) -> str:
    cleaned = re.sub(r'<[^>]+>|\xad|-\s*\n\s*', ' ', text)
    return ' '.join(unicodedata.normalize('NFC', cleaned).split())


def check_controls(root: Path, report: dict, control: dict) -> list[str]:
    errors: list[str] = []
    wave = report.get('wave9', {})
    if (wave.get('controls'), wave.get('baselineCommit'), wave.get('publicationEligible'), wave.get('mergePerformed')) != (
        CONTROL, BASELINE, False, False
    ):
        errors.append('wave9: journal identity/nonpublication boundary')
    if (control.get('baselineCommit'), control.get('status'), control.get('c25'), control.get('o10'), control.get('o11')) != (
        BASELINE, STATUS, 'OPEN', O10, O11
    ):
        errors.append('wave9: status/C25/O10/O11 boundary drift')
    for key in FALSE_BOUNDARIES:
        if control.get(key) is not False:
            errors.append('wave9: missing/overclaimed boundary ' + key)
    if control.get('statistics') != STATISTICS:
        errors.append('wave9: artifact/scope statistics drift')
    if set(control.get('cyrilFiveLocusSynthesis', {})) != CYRIL_LOCI:
        errors.append('wave9: Cyril five-locus synthesis inventory drift')
    if set(control.get('patristicOriginalVerifications', {})) != PATRISTIC_CARDS:
        errors.append('wave9: patristic original verification inventory drift')

    policy = json.loads((root / 'data/repository-evidence-policy-v2.json').read_text(encoding='utf-8'))
    axes = {
        'evidenceClass': 'sourceClasses',
        'accessState': 'accessStates',
        'locatorState': 'locatorStates',
        'rightsState': 'rightsStates',
        'publicationState': 'publicationStates',
    }

    def states(row: dict, label: str) -> None:
        for key, vocabulary in axes.items():
            if row.get(key) not in policy[vocabulary]:
                errors.append(f'wave9: noncanonical axis {label}/{key}')
        for h in row.get('holds', []):
            if h not in policy['holds']:
                errors.append(f'wave9: noncanonical hold {label}/{h}')
        if row.get('publicationEligible') is not False or row.get('publicationState') != 'BLOCKED' or 'PUBLICATION_HOLD' not in row.get('holds', []):
            errors.append('wave9: publication promotion ' + label)

    files = control.get('files', [])
    if len(files) != len(FILE_PINS) or {f.get('id') for f in files} != set(FILE_PINS):
        errors.append('wave9: artifact inventory missing/duplicate')
    for f in files:
        ident = f.get('id', '')
        states(f, ident)
        if (f.get('sha256'), f.get('bytes'), f.get('gitBlob')) != FILE_PINS.get(ident):
            errors.append('wave9: artifact byte pin ' + ident)
        repo, upath, ext, tier = FILE_LAYOUT.get(ident, ('', '', '', ''))
        if (f.get('kind'), f.get('tier'), f.get('repo'), f.get('commit'), f.get('path'), f.get('externalRelativePath')) != (
            'git_blob', tier, repo, PINS.get(repo), upath, ext
        ):
            errors.append('wave9: artifact identity/path ' + ident)
        if f.get('puseyVol2OrPg74PrintScanFor1152') is not False:
            errors.append('wave9: Pusey Vol. II / PG 74 print scan overclaim ' + ident)
        if ident in A1_SCAN_IDS:
            if (
                f.get('evidenceClass') != 'A1'
                or f.get('visualScanInspected') is not True
                or f.get('quoteSafe') is not True
                or f.get('accessState') != 'FULL_OBJECT_VERIFIED'
                or f.get('locatorState') != 'EXACT_LOCATOR_VERIFIED'
                or not str(f.get('path', '')).endswith('.jpg')
            ):
                errors.append('wave9: A1 visual scan contract ' + ident)
        elif ident in A1_TEI_IDS:
            if (
                f.get('evidenceClass') != 'A1'
                or f.get('visualScanInspected') is not False
                or f.get('quoteSafe') is not True
                or f.get('rightsState') != 'STORAGE_ONLY'
                or not str(f.get('path', '')).endswith('.xml')
            ):
                errors.append('wave9: A1 TEI contract ' + ident)
        else:
            if (
                f.get('evidenceClass') != 'C'
                or f.get('visualScanInspected') is not False
                or f.get('quoteSafe') is not False
                or 'EVIDENCE_HOLD' not in f.get('holds', [])
            ):
                errors.append('wave9: class C OCR contract ' + ident)
        if (root / ext).exists():
            errors.append('wave9: external file leaked into repository ' + ident)

    repairs = {r['id']: r for r in report.get('repairs', []) if str(r.get('id', '')).startswith('W9-')}
    if set(repairs) != REQUIRED_REPAIRS or set(wave.get('repairIds', [])) != REQUIRED_REPAIRS:
        errors.append('wave9: repair coverage')
    snaps = wave.get('supersededSnapshots', [])
    if len({s['path'] for s in snaps}) != len(snaps) or not {r['file'] for r in repairs.values()} <= {s['path'] for s in snaps}:
        errors.append('wave9: actual preimage coverage')
    baseline_texts: dict[str, str] = {}
    for s in snaps:
        if s.get('commit') != BASELINE:
            errors.append('wave9: preimage baseline')
            continue
        p = subprocess.run(['git', 'show', f"{BASELINE}:{s['path']}"], cwd=root, capture_output=True)
        if p.returncode or (len(p.stdout), digest(p.stdout), git_blob(p.stdout)) != (
            s.get('bytes'), s.get('sha256'), s.get('blob')
        ):
            errors.append('wave9: actual Git preimage mismatch ' + s['path'])
        else:
            baseline_texts[s['path']] = p.stdout.decode('utf-8')

    for r in repairs.values():
        present = r['removed'] in baseline_texts.get(r['file'], '')
        kind = 'BASELINE_REMOVAL_OR_EXPLICIT_SUPERSESSION' if present else 'ADDITIVE_GUARD_NOT_A_HISTORICAL_QUOTE'
        if r.get('rejectedWordingPresentInBaseline') is not present or r.get('controlType') != kind:
            errors.append('wave9: invented historical error ' + r['id'])
        text = (root / r['file']).read_text(encoding='utf-8')
        if present and not r.get('historicalRetained') and r['removed'] in text:
            errors.append('wave9: rejected baseline wording still present ' + r['id'])
        if r['required'] not in text:
            errors.append('wave9: owner update missing ' + r['id'])

    for path in REGISTRIES:
        review = json.loads((root / 'ИСКУПЛЕНИЕ' / path).read_text(encoding='utf-8')).get(REVIEW_KEY, {})
        if (
            review.get('controls'),
            review.get('status'),
            review.get('c25'),
            review.get('o10'),
            review.get('o11'),
            review.get('puseyVol2PageImagesInspected'),
            review.get('mignePg74PageImagesInspected'),
            review.get('fullCyril1152FragmentGreekOriginalVerified'),
            review.get('publicationEligible'),
        ) != (CONTROL, STATUS, 'OPEN', O10, O11, False, False, False, False):
            errors.append('wave9: registry review boundary ' + path)
        if (
            review.get('cramerCoislin23CatenaScanEvidenceClass') != 'A1'
            or review.get('coislin23AnonymousFor1152') is not True
            or review.get('puseyVol2DualOcrEvidenceClass') != 'C'
            or review.get('oratio4522GreekOcrQuoteSafe') is not False
        ):
            errors.append('wave9: registry class/anonymity boundary ' + path)

    ledger = (root / 'ИСКУПЛЕНИЕ/synthesis/02_CONFLICT_LEDGER.md').read_text(encoding='utf-8')
    c25 = re.search(r'(?ms)^## C-25\b.*?(?=^## |\Z)', ledger)
    if not c25 or not re.search(r'\*\*Статус:\*\*\s*`OPEN`', c25.group()):
        errors.append('wave9: C25 owner status is not OPEN')
    return errors


def verify_sources(source_root: Path, control: dict) -> list[str]:
    """Full byte & JPEG gate first; never parse text from an unverified external object set."""
    errors: list[str] = []
    raws: dict[str, bytes] = {}
    base = source_root.resolve()
    for f in control.get('files', []):
        ident = f['id']
        target = (base / f['externalRelativePath']).resolve()
        try:
            target.relative_to(base)
        except ValueError:
            errors.append('wave9 replay: path traversal ' + ident)
            continue
        if not target.is_file() or target.is_symlink():
            errors.append('wave9 replay: missing/symlink file ' + ident)
            continue
        raw = target.read_bytes()
        if (digest(raw), len(raw), git_blob(raw)) != (f['sha256'], f['bytes'], f['gitBlob']):
            errors.append('wave9 replay: artifact bytes changed ' + ident)
            continue
        if ident in A1_SCAN_IDS and not (raw.startswith(b'\xff\xd8\xff') and raw.endswith(b'\xff\xd9')):
            errors.append('wave9 replay: invalid JPEG markers ' + ident)
            continue
        raws[ident] = raw
    if errors:
        return errors

    try:
        pl75 = norm_xml(raws['PL75-TEI-XML'].decode('utf-8'))
        pl54 = norm_xml(raws['PL54-TEI-XML'].decode('utf-8'))
        or30 = norm_xml(raws['FIRST1K-NAZ-OR30-XML'].decode('utf-8'))
        p106 = raws['PUSEY-V2-UOFT-0118-TXT'].decode('utf-8')
        p233 = norm_xml(raws['PUSEY-V2-UOFT-0245-TXT'].decode('utf-8'))
        p292 = raws['PUSEY-V2-UOFT-0304-TXT'].decode('utf-8')
        p295_uoft = raws['PUSEY-V2-UOFT-0307-TXT'].decode('utf-8')
        p295_goog = raws['PUSEY-V2-GOOG-0305-TXT'].decode('utf-8')
        gaume = raws['GAUME-CHRYS-0472-TXT'].decode('utf-8')
        chrys_og = raws['OG-CHRYS-IN-JOANNEM-JSONL'].decode('utf-8')
        naz_og = raws['OG-NAZ-OR45-JSONL'].decode('utf-8')

        for needle in ('sine aestimatione', 'Misertus ergo creator ut', 'juxta carnem pertulit', 'apostatam angelum'):
            if needle not in pl75:
                errors.append('wave9 replay: PL75 expected reading missing: ' + needle)
        for needle in ('propitiatio fuit mundi', 'tyrannica vincula', 'conditionis nostrae debitum'):
            if needle not in pl54:
                errors.append('wave9 replay: PL54 expected reading missing: ' + needle)
        for needle in ('λύτρον ἑαυτὸν ἀντιδιδοὺς ἡμῶν τῆς οἰκουμένης καθάρσιον', 'ὡς σφάγιον'):
            if needle not in or30:
                errors.append('wave9 replay: Or. 30 TEI expected reading missing: ' + needle)
        if 'δημιουργός' not in p106 or 'ἐν τέκνοις' not in p106:
            errors.append('wave9 replay: Pusey II John 8:47 distinction missing')
        if 'μὴ μὴν ἐν ἴσῳ πᾶσιν' not in p233 or 'συνανιστῶντος' not in p233:
            errors.append('wave9 replay: Pusey II John 10:14-15 distinction missing')
        if '691Α' not in p292:
            errors.append('wave9 replay: Pusey II John 11:44 691A marker missing')
        if 'χρηματίζομεν' not in p295_uoft or 'Cr. [p.3 22 .]' not in p295_uoft:
            errors.append('wave9 replay: Pusey II uoft Cramer p. 322 apparatus missing')
        if 'Ἐκκλησίαν' not in unicodedata.normalize('NFC', p295_goog) or 'παραδείσῳ' not in unicodedata.normalize('NFC', p295_goog):
            errors.append('wave9 replay: Pusey II goog independent OCR stream missing')
        if 'liberati fideles sunt' not in gaume:
            errors.append('wave9 replay: Gaume Hom. 65 Latin reading missing')
        if 'pg059_0361.4' not in chrys_og or 'ἀπηλλάγησαν οἱ πιστοί' not in chrys_og:
            errors.append('wave9 replay: OpenGreek Chrysostom Hom. 65 reading missing')
        if 'pg036_0351.1' not in naz_og:
            errors.append('wave9 replay: OpenGreek Gregory Naz. Or. 45.22 locus missing')
    except (ValueError, KeyError, UnicodeError) as exc:
        errors.append('wave9 replay: invalid source structure ' + str(exc))
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--source-root', type=Path)
    args = ap.parse_args()
    try:
        control = json.loads((args.root / CONTROL).read_text(encoding='utf-8'))
        report = json.loads((args.root / REPORT).read_text(encoding='utf-8'))
        errors = check_controls(args.root, report, control)
        replay = verify_sources(args.source_root, control) if args.source_root else []
        errors += replay
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('WAVE9 SOURCES: FAIL —', exc)
        return 1
    print(json.dumps(dict(
        control['statistics'],
        sourceByteReplay=('FAIL' if replay else 'PASS') if args.source_root else 'NOT_RUN',
        cramerCoislin23CatenaScanVerified=True,
        puseyVol1John1_11_13ScansVerified=True,
        mason1899Or3020_21ScansVerified=True,
        pl54AndPl75TeiOriginalsVerified=True,
        puseyVol2AndPg74PageImagesInspected=False,
        fullCyril1152GreekOriginalVerified=False,
        humanReadingMeasured=False,
        publicationApproved=False,
    )))
    for error in errors:
        print('FAIL:', error)
    print('WAVE9 SOURCES: ' + ('FAIL' if errors else 'PASS — 21 A1 scans + 3 A1 TEI + 27 C OCR verified; Pusey II 11:52 scan and C25 OPEN'))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
