# Project language: replies, canvas artifacts and native decisions

## Set and retain the user-facing language

Apply this contract BEFORE producing replies, artifacts or Question cards, including on resume. Latest explicit user display/output-language instructions take precedence. Otherwise use the language of the user's substantive natural-language project request: an English request means English replies AND English agent-authored canvas content and decisions; a Chinese request means Chinese by default. Do not infer language from quoted reference text, URLs, code, a film title, search results, style-library language, tool output, this Skill's Chinese examples, invocation metadata or a one-word answer to an existing card. For an existing project retain its established language unless a substantive user-language switch or explicit instruction changes it; do not reopen a routine language questionnaire. Resolve a genuine conflicting requirement with one focused native choice only when necessary.

Persist the interface/artifact display language with project state and pass it to each actual worker/tool-writing task. Track dialogue/narration and subtitle language separately when the user explicitly requests something different. By default new story prose, new dialogue and captions follow the project language. Preserve exact user-supplied/approved lines, names and intentionally foreign quotations when required; interface localization alone does not authorize translating approved spoken content, renaming identities or regenerating voices/video. Explicit multilingual dialogue or bilingual captions are an intentional exception, not permission for arbitrary mixed-language table labels.

This contract overrides literal display wording in all bundled references. Chinese gate titles, column names, choice examples, status words and document-title examples are SEMANTIC KEYS, not mandatory UI strings. Internal tool names, enum values, payload keys, actual IDs, asset handles, file paths, code and model identifiers must retain their real schema values. Do not translate API arguments or invent localized APIs. Native parameter/control names also retain their exact native spelling/case (e.g. quality and image area); localize explanations, not parameter names. See image-settings.md. Platform-owned buttons such as Other and fixed host error text may not be under agent control; translate the agent's explanations while preserving necessary exact technical evidence. Do not claim the Skill changes the host application's locale.

## All agent-authored surfaces

Use the resolved language consistently for replies, progress/recovery explanations, canvas node/document titles, brief/Mood-board notes and keywords, new scripts and shot scripts, character/scene/prop labels and design descriptions, voice-profile explanations, table headings AND every narrative cell, page indexes, notes, status annotations, preview/revision explanations, editor track/clip labels where editable, final handoff and download labels. Render style choices using their corresponding English names/categories for English projects rather than copying bilingual catalog rows. Preserve stable underlying style slugs and role/scene/shot IDs. Proper names may use established user-approved display names; do not invent new character identities to remove a script-mandated foreign name.

Question titles, locating questions, descriptions, options and modification prompts use the SAME language. Scripts and tables stay fully saved/read back ON CANVAS; localization never moves their body into a card. For English: Script Review; Character / Scene / Prop Design Review (applicable types only); Family Reference Character Review; Voice Preferences; Voice Audition Review; Shot Production Table Review; Shot Review; Post-production Options; Final Edit Review; Edit Instructions; Recovery. Keep actual gate IDs/approval semantics and scope unchanged. Use concise localized actions such as Approve and continue / Request changes / View again. Table review: Approve and generate all shots / Revise a shot or image / View table and storyboards again. Final edit: Approve and export / Request changes / Preview again. Post options: Stitch only / Subtitles only / Stitch + subtitles (recommended) plus the actual native Other field. Never infer approval from a translated recommendation or add duplicate language-specific gates.

## Nine-column shot production table

For an ENGLISH project, canvas title is **Shot Production Table** (with film title/version as needed) and EVERY page uses exactly these nine visible headers in this order:

| Scene / Shot ID | Start Time | End Time | Visual Description | Dialogue | Shot Size | Focal Length Rationale | Background Music | Sound Effects |
|---|---|---|---|---|---|---|---|---|

Their semantic mapping to the existing contract is:
- Scene / Shot ID = 场景／镜头 ID
- Start Time = 开始时间
- End Time = 结束时间
- Visual Description = 画面描述 (one column only)
- Dialogue = 台词
- Shot Size = 景别
- Focal Length Rationale = 镜头焦段判断
- Background Music = BGM
- Sound Effects = 音效

For Chinese projects use the corresponding Chinese labels; for other languages localize the same nine concepts and preserve their order/IDs. Do not add parallel Chinese headers, slash-separated bilingual headings or an extra translation column unless explicitly requested. The mapping above is internal instruction, never a bilingual output template.

English CELL VALUES must also be English, including scene/action descriptions, reasons, speech-role labels, music/effects cues and empty/not-applicable states. Use e.g. **No dialogue**, **Dialogue**, **Off-screen dialogue**, **Narration**, **Close-up**, **Wide shot**, **Not applicable (2D / orthographic; ...)**, **Post-production music: ...**, **No music**, **Sound effects: ...**, **Intentional silence**, **Planned**, **Pending**, **Approved** rather than copying 无台词、旁白、特写、不适用、后期独立配乐、无音效、待确认. Write a concrete action and lens rationale in English; preserve technical values such as 16:9, 35 mm, HH:MM:SS and actual IDs. Do not invent dialogue to fill a cell. Exact approved foreign-language dialogue may remain only when required by the user's content/translation instructions, with surrounding labels/explanations in English.

## Readback, revisions and existing mixed-language canvases

Before displaying or asking for approval, read the ACTUAL saved current canvas artifact: inspect every table page, all nine headers and every narrative cell, titles, indexes/status notes, related previews and agent-authored card text for language consistency. A translated prompt or first row is not proof the saved table was translated. Classify retained names, technical tokens and explicitly multilingual lines before treating foreign script as a defect; a blanket non-ASCII ban is wrong. Repair unintended untranslated fragments through real native updates and read back again before issuing a concise localized card. Do not hide the problem by summarizing or omitting rows.

On resume, repair an existing mixed-language table in the SAME logical canvas artifact. Preserve all shots, columns, IDs, source mappings, exact approved content and media, timing, references and coverage. Save the new display revision/readback evidence; update any awaiting card to the matching artifact version, discarding stale responses. A faithful display-only translation of headings/explanations does not trigger paid asset regeneration or reapproval of unchanged story/voices/images. If translating dialogue or changing story meaning is requested, follow the existing relevant revision/approval gates and update only real dependents. Saved terminology or earlier Chinese examples cannot override the active language. Maintain this consistency through final editing and export.
