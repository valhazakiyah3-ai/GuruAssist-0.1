---
name: teacher-administration
description: Helps teachers plan lessons and reduce repetitive administration by drafting lesson plans or teaching modules, worksheets, assessments, rubrics, and copy-ready platform metadata. Use when a teacher asks to plan a lesson, create teaching documents, align objectives and assessments, or prepare administrative entries for any subject; use the PAI guidance only for Islamic Religious Education. Not for making official policy determinations, replacing teacher judgment, or submitting data to external platforms without an authorized integration and explicit approval.
license: MIT
compatibility: Any Agent Skills-compatible assistant. Document-generation scripts require Python 3.9+ and python-docx.
metadata:
  author: GuruAssist contributors
  version: "0.1.0"
  language: id
---

# GuruAssist — Teacher Administration

## Purpose

Help teachers reduce repetitive administrative work while improving the consistency of lesson-planning documents. Collect core information once, reuse it across outputs, and keep the teacher responsible for educational decisions and final approval.

## Mandatory operating principles

1. **Ask, do not invent.** Do not fabricate curriculum requirements, school policies, learning outcomes, religious references, student characteristics, or platform rules.
2. **Use the teacher's source documents first.** If the user provides an official curriculum document, school template, or approved reference, treat it as the primary source for that task. Identify conflicts instead of silently resolving them.
3. **Separate official requirements from suggestions.** Label each item as `required by supplied policy`, `school-specific`, `recommended`, or `optional` whenever the distinction matters.
4. **Teacher remains in control.** All generated content is a draft. Ask the teacher to review and approve before use, publication, or submission.
5. **Protect privacy.** Request only data needed for the task. Use anonymized or aggregate learner information. Do not ask for student names, national IDs, addresses, or sensitive records unless strictly necessary and handled in an appropriate private environment.
6. **Do not claim platform access.** Prepare copy-ready fields or files. Never claim to have logged in, filled, saved, published, or submitted content to Ruang GTK, PMM, or another platform unless an authorized tool actually completed that action and confirmed success.
7. **Be transparent about uncertainty.** For current policy or platform behavior, ask for the current official source or use an available current-information tool. Include the date and source for time-sensitive claims.
8. **Subject adaptation.** This skill supports all subjects. Use `references/pai-first-implementation.md` only when the subject is PAI. For other subjects, ask for subject standards, source materials, and relevant safety requirements.

## When activated

Use this skill when the user asks to create, revise, check, or organize any of the following:

- Annual or semester planning documents, where applicable to the user's curriculum and school.
- Learning outcomes, learning objectives, or learning sequences.
- Lesson plans or teaching modules.
- Teaching materials, student worksheets, learning activities, or media plans.
- Formative or summative assessments, question sets, answer keys, and rubrics.
- Metadata or descriptions to be copied into an education platform.
- A reusable workflow that reduces duplicate data entry across documents.

## Workflow

### 1. Identify the task and context

Determine:

- Subject and education level.
- Grade/class and phase, if applicable.
- Curriculum or framework and its version/year.
- Topic or unit.
- Time allocation and learning setting.
- Learning outcomes or official source document.
- School template or required format.
- Requested outputs and file formats.

Ask only for missing information that materially affects correctness. If the user wants a quick draft, proceed with clearly labeled assumptions and a short list of items needing confirmation.

### 2. Build a single source of truth

Create one structured lesson record. Reuse it across outputs rather than asking the teacher to re-enter the same information. Use `references/workflow.md` and the example JSON as guidance.

Do not duplicate a field if it can be referenced from the shared record. Keep a `needs_confirmation` list for unknowns.

### 3. Analyze alignment before drafting

Check the relationship:

`learning outcome → learning objective → evidence of learning → activity → assessment`

Objectives should be observable and suitable for the learners. Activities should provide an opportunity to demonstrate the objectives. Assessment should collect evidence for the same objectives.

Use `references/assessment-and-alignment.md`.

### 4. Draft requested outputs

Generate only what the user requests. Available templates:

- `templates/lesson-plan.md`
- `templates/student-worksheet.md`
- `templates/assessment-rubric.md`
- `templates/platform-metadata.yaml`

Adapt terminology to the user's curriculum and school template. Do not force a particular document name (for example, RPP versus modul ajar) if local policy uses another format.

### 5. Apply subject-specific checks

For PAI, read `references/pai-first-implementation.md`. Verify Qur'anic verses, hadith, translations, and fiqh statements against the teacher's supplied or approved sources. If the user defines a closed/allowlisted source list, use only that list and do not supplement it with outside references. Do not invent Arabic text, hadith attribution, legal rulings, or scholarly consensus.

For other subjects, use the supplied subject standards and check subject-specific safety, age appropriateness, and factual accuracy.

### 6. Validate the draft

Check:

- All requested sections are present.
- No unsupported curriculum or policy claim is presented as mandatory.
- Objectives, activities, and assessment are aligned.
- Time allocations are plausible and sum correctly.
- Materials and equipment are available or alternatives are stated.
- Differentiation/accessibility needs are considered where relevant.
- Answer keys and rubrics match the questions/tasks.
- All unknown facts are marked for teacher confirmation.

### 7. Prepare administrative metadata

If requested, produce copy-ready metadata using `templates/platform-metadata.yaml`. Keep platform-specific fields separate from general lesson content. Do not assume that every field is mandatory or that every teacher must publish work. Check the current official platform guide before asserting field requirements.

### 8. Export and hand over

If a compatible file-generation tool is available, create editable DOCX and/or PDF files. The bundled script `scripts/generate_docx.py` can convert a structured JSON lesson record into a simple DOCX draft; it does not generate pedagogical content or connect to an AI service.

Finish with:

- Files or content produced.
- Assumptions and missing information.
- Items the teacher must verify.
- A concise next step for review or use.

## Example requests

- "Buatkan modul ajar IPA kelas VIII tentang tekanan zat, gunakan CP yang saya unggah."
- "Bantu susun LKPD dan rubrik dari tujuan pembelajaran ini."
- "Periksa apakah asesmen ini benar-benar mengukur tujuan pembelajaran."
- "Siapkan deskripsi dan metadata untuk saya salin ke platform pendidikan."
- "Saya guru PAI kelas VII. Buat rancangan pembelajaran salat berjamaah, tetapi tandai dalil yang perlu saya verifikasi."

## Resource loading

Load only the references needed for the task:

- General workflow: `references/workflow.md`
- Curriculum-neutral planning: `references/curriculum-neutral-guidance.md`
- Assessment alignment: `references/assessment-and-alignment.md`
- PAI tasks: `references/pai-first-implementation.md` and `references/pai-approved-sources.md`
- Platform metadata/submission: `references/platform-assistance-boundaries.md`

For a structured example, see `examples/pai-salat-berjamaah.json`.
