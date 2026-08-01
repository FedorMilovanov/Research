import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const archivePath = 'incoming/arena-auditor/2026-07-09/GILL_SERIES_EVIDENCE_ARCHIVE_V1_V11_001_480_2026-07-09.md';
const matrixPath = 'Джон Гилл/74_PR2_001_480_RECONCILIATION_MATRIX.md';
const navPath = 'Джон Гилл/00_README_AND_NAVIGATION.md';
const expectedArchiveBlob = 'baa3fccb6f67cd05117b2c4f0342867662a3fce0';
const expectedMatrixBlob = '90085ab3d75ebc51f0c398fd3a8e2b4f4674a824';
const expectedSiteMerge = '877508fbfe42883b99922e3dcc717adfa91c33ad';
const expectedExactHead = '433c76ddd4ee37e9efe8fd4f5fc7573aa8e2a736';

const archive = fs.readFileSync(archivePath, 'utf8');
const matrix = fs.readFileSync(matrixPath, 'utf8');
const nav = fs.readFileSync(navPath, 'utf8');
const failures = [];

function git(...args) {
  try {
    return execFileSync('git', args, { encoding: 'utf8' }).trim();
  } catch (error) {
    failures.push(`git ${args.join(' ')} failed: ${error.stderr?.toString().trim() || error.message}`);
    return '';
  }
}

function idsFrom(text, pattern) {
  return [...text.matchAll(pattern)].map((match) => Number(match[1]));
}

function assertSequence(ids, label) {
  if (ids.length !== 480) failures.push(`${label}: expected 480 IDs, found ${ids.length}`);
  for (let index = 0; index < ids.length; index += 1) {
    if (ids[index] !== index + 1) {
      failures.push(`${label}: expected ID ${index + 1}, found ${ids[index]}`);
      break;
    }
  }
}

// Compute Git object IDs from actual bytes. Literal blob markers alone are not evidence.
const archiveWorkingBlob = git('hash-object', archivePath); // git hash-object is required by repository integrity gate
const archiveHeadBlob = git('rev-parse', `HEAD:${archivePath}`);
const matrixWorkingBlob = git('hash-object', matrixPath);
const matrixHeadBlob = git('rev-parse', `HEAD:${matrixPath}`);
if (archiveWorkingBlob !== expectedArchiveBlob) failures.push(`archive working blob drift: ${archiveWorkingBlob} != ${expectedArchiveBlob}`);
if (archiveHeadBlob !== expectedArchiveBlob) failures.push(`archive HEAD blob drift: ${archiveHeadBlob} != ${expectedArchiveBlob}`);
if (matrixWorkingBlob !== expectedMatrixBlob) failures.push(`matrix working blob drift: ${matrixWorkingBlob} != ${expectedMatrixBlob}`);
if (matrixHeadBlob !== expectedMatrixBlob) failures.push(`matrix HEAD blob drift: ${matrixHeadBlob} != ${expectedMatrixBlob}`);
if (git('status', '--porcelain', '--', archivePath, matrixPath, navPath)) failures.push('Gill reconciliation inputs are dirty');

assertSequence(idsFrom(archive, /^## GILL-CONTENT-(\d{3})\s+—/gm), 'archive');
assertSequence(idsFrom(matrix, /^\| GILL-CONTENT-(\d{3}) \|/gm), 'matrix');
if (Buffer.byteLength(archive, 'utf8') < 400_000) failures.push('archive: unexpectedly smaller than 400 KB');

const archiveMarker = matrix.match(/\*\*Archive blob:\*\* `([0-9a-f]{40})`/i)?.[1];
if (archiveMarker !== archiveWorkingBlob) failures.push(`matrix archive marker ${archiveMarker} != actual blob ${archiveWorkingBlob}`);
if (!matrix.includes(`merge \`${expectedSiteMerge}\``)) failures.push('matrix: site PR192 merge marker missing');
if (!matrix.includes(`exact head \`${expectedExactHead}\``)) failures.push('matrix: exact-head CI marker missing');
for (const commit of [expectedSiteMerge, expectedExactHead]) {
  git('cat-file', '-e', `${commit}^{commit}`);
}
if (!nav.includes('| 74 | `74_PR2_001_480_RECONCILIATION_MATRIX.md` |')) failures.push('navigation: volume 74 row missing');
if (!nav.includes('`70`–`74`.')) failures.push('navigation: primary-verifiability cluster does not include volume 74');

const dossierChecks = [
  ['Джон Гилл/01_SERIES_GAPS_AND_PRIMARY_SOURCES.md', ['ИСТОРИЧЕСКОЕ ДОСЬЕ / SUPERSEDED'], ['1769–1773, 3 книги', 'крупнейший библейский комментарий одного автора']],
  ['Джон Гилл/03_STRUCTURE_PROPOSAL.md', ['ИСТОРИЧЕСКОЕ ДОСЬЕ / SUPERSEDED'], []],
  ['Джон Гилл/04_CONTENT_DEEPENING_AUDIT_AND_EXEGESIS_SET.md', ['Book II, ch. 7', 'Part IV (1738):'], ['Body of Divinity Book IV); вечное оправдание', 'природа, виды и случаи божественного просвещения']],
  ['Джон Гилл/06_SITE_INDEX_LAW_ANTINOMIANISM_ELECTION.md', ['издан в трёх печатных томах', 'Девять томов относятся'], ['Body of Divinity*, 9 томов / 7 книг']],
  ['Джон Гилл/20_HEBREW_PRIESTHOOD_AND_PUBLIC_SINGING.md', ['УТОЧНЕНИЕ ПО ПЕНИЮ'], ['охватывают как божественные псалмы Давида, так и новозаветные евангельские гимны']],
  ['Джон Гилл/25_COVENANT_ARCHITECTURE_VERBATIM.md', ['Witsius принадлежал к более позднему голландскому поколению', 'не автоматически принятая современная этимология'], ['Goodwin/Witsius/Twisse — ведущие делегаты Вестминстерской ассамблеи']],
  ['Джон Гилл/26_CHRISTIAN_GOOD_WORKS_AND_ETHICS.md', ['FALSE-GREEN СНЯТ', 'по милости Божьей'], ['dissertationconc00gill)),', 'по мистии Божьей']],
  ['Джон Гилл/28_GOSPEL_MIRACLES_APOLOGETICS.md', ['ИСТОЧНИКОВАЯ КАЛИБРОВКА', 'Свидетельство служителей'], ['Свидетельство водоносов', 'фарисеев и саддукеев, пришедших утешать']],
  ['Джон Гилл/32_NEONOMIANISM_MARROW_CONTROVERSY.md', ['КАНОНИЧЕСКАЯ ПОПРАВКА', 'принимающий вменённую праведность', 'источники не устанавливают «два крыла одного фронта»'], ['接收ающий', 'Marrow = шотландское крыло']],
  ['Джон Гилл/39_THE_PNEUMATOLOGY_SPIRIT_APPLICATION.md', ['ПРЕДУПРЕЖДЕНИЕ О CCEL-МАРШРУТАХ'], []],
  ['Джон Гилл/40_THE_CHRISTOLOGY_PERSON_OF_CHRIST.md', ['ПРЕДУПРЕЖДЕНИЕ О CCEL-МАРШРУТАХ'], []],
  ['Джон Гилл/42_THE_CREATION_IMAGE_OF_GOD_AND_PROVIDENCE.md', ['ПРЕДУПРЕЖДЕНИЕ О CCEL-МАРШРУТАХ'], []],
];

for (const [path, required, forbidden] of dossierChecks) {
  const text = fs.readFileSync(path, 'utf8');
  for (const marker of required) if (!text.includes(marker)) failures.push(`${path}: required marker missing: ${marker}`);
  for (const marker of forbidden) if (text.includes(marker)) failures.push(`${path}: forbidden stale marker remains: ${marker}`);
}

if (failures.length) {
  console.error(`Gill PR2 lossless reconciliation: FAIL (${failures.length})`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}
console.log('Gill PR2 lossless reconciliation: PASS — archive and matrix blobs verified, 480 IDs reconciled, commit witnesses present.');
