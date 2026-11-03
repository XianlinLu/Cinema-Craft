# Audible shots, separate sound roles and native final scoring

## Mandatory sound contract

**BGM-free means no model-generated background score; it NEVER means all sound is muted.** For every shot, infer the intended audible content from the approved script, exact lines, visible actions, setting and shot table. Preserve character dialogue, off-screen dialogue, narration, required foley/sound effects and intended ambience. A shot without visible speakers can still need narration or off-screen speech; a shot without dialogue can still need effects/ambience. Only an explicitly justified intentional-silence interval may be soundless. Do not add gratuitous sounds or dialogue absent from the approved story.

Apply this contract before shot review, continuation reuse, final editor import and delivery. A completed generation task, an audio stream, a waveform or a subtitle is not proof that the intended sound is actually audible. Never hand the user a silent speaking shot with a promise to restore it only during final editing. A separate sound-production route must be composed into a real audible prepared shot before the native shot-confirmation card. This rule takes precedence over shorter mute/silent-picture examples in other resources.

## Plan sound with each shot

Keep a conceptual sound map alongside each production row, using supported project metadata rather than invented tool fields:

- Speech: exact line IDs/text, speaker and approved voice versions, actual audio asset, on/off-screen/narrator role, measured start/end, required mouth synchronization.
- Effects/ambience: meaningful events and source IDs, such as steps, contact/impact, door movement, room tone or weather when the scene calls for them; cue times, duration, gain and whether retained from the successful source or separately produced.
- Model BGM: absent, isolated for removal, or mixed and requiring actual separation/reconstruction. A failed or unknown cleanup is not an absence check.
- Final score: added later as a separate whole-film music track, never baked into prepared source shots. Do not attach final score files as voice references.
- Silence: only the intentional interval and its approved narrative reason, with speech/effect expectations explicitly empty there. An empty plan caused by missing analysis is not intentional silence.

Prefer native integrated generation with approved voices, exact dialogue and scene effects while requesting no background music through actual supported controls and the prompt. There may be no music-only switch: do not invent one or confuse a global audio switch with BGM removal. If using a separately planned picture/speech/effects route, resolve real generation, synchronization and composition capabilities before submitting. Picture-only output is intermediate, not a reviewable final shot.

## Remove music without losing voices or effects

Process only successfully released media. Preserve raw originals, their metadata and actual asset IDs.

1. **No BGM present:** retain the correct source speech, effects and ambience; do not mute merely because this stage is called cleanup. Verify the actual playback.
2. **Real separate music stem:** mute/remove only that stem. Retain dialogue, narration, effects and ambience at their intended levels. Check the operation did not also mute the clip/group/project or unrelated tracks.
3. **Mixed soundtrack:** use a genuine native music-separation operation if exposed, then inspect for lost consonants, effects, artifacts or residual music. A label named audio or a gain control is not a stem separator.
4. **Separation unavailable or destructive:** full-mix mute is permitted only as an INTERMEDIATE reconstruction step. Within the same preparation job, restore exact approved character/narrator audio and retain/reconstruct required effects/ambience through actual native tools and cue timing. Include correct lips for visible speech. Muting the mix and restoring speech alone is incomplete when the shot also needs effects. Keep the job out of QC_READY until the actual prepared playable result contains the complete intended sound and no model BGM.
5. **No supported way to complete this:** record a precise capability blocker and use native recovery for the affected shot. Preserve other successful work. Do not deliver silence, invent a separated stem, substitute another person's voice, or regenerate all approved pictures as a routine workaround.

If a required effect is lost during cleanup, first recover it from a successful original/separated source where possible; otherwise produce a matching original/cleared effect with native sound tools, preserve the planned action cue, and inspect the result. Technical restoration preserving the approved sound plan continues automatically. A new creative sound/line/voice change revisits only its relevant native gate. Never recover blocked output or change audio routes to bypass a provider rejection; the existing policy-recovery rules still apply.

The prepared-shot preview must actually play picture AND its composed speech/effects together, through a real prepared clip or supported synchronized native preview. An unconnected audio asset next to a soundless video, a row in the table, or a claimed future mix does not meet this requirement. Record the preview composition and audio versions as part of the shot's approved version. Clip-only delivery must itself contain the approved sound. A source-only continuation handle remains tied to the correct prepared version and sound map; do not lose the next shot's speech/effects or repeat the predecessor's lines when trimming extension prefixes.

## Sound acceptance before every shot card

Inspect actual prepared playback and available native media analysis. Distinguish failures in the asset from a muted player/output device. Do not claim listening or analysis if the host exposes neither.

- All expected lines are present, audible and intelligible, in the correct approved voices; narration/off-screen lines are included even when no mouth is visible.
- Visible speech matches the picture; no doubled original-plus-restored voice, missing words, wrong speaker or forced speech speed.
- Necessary sound effects and ambience remain audible at the intended moments and are not confused with unwanted music. No accidental whole-clip mute or missing/disabled audio track.
- No model BGM remains in the prepared source; check actual audio rather than relying on the prompt. Quiet intentional pauses are preserved and not filled automatically.
- Duration, cue offsets and trims match the shot; extension prefixes contain no repeated lines/effects in the selected new span.

Store expected sound roles, actual retained/restored assets, preparation IDs, audible-check evidence and version in the manifest. If expected speech/effects are missing or the audible check is unavailable, the shot does not meet QC_READY and must not receive an ordinary “Approve this shot” review as if complete. Repair technical omissions automatically within existing bounds, then recheck. If an already approved silent shot is being fixed, create a corrected version and repeat only the affected shot/dependent approvals; never keep stale approval for a changed soundtrack.

## Automatic scoring in native Video Editor

Once all current shots are approved and the native post-production scope is selected, automatically prepare suitable final scoring as part of the authorized edit. Infer a short music brief from actual story mood, selected visual style, scene progression, dialogue density, pace, dramatic peaks and ending. Choose fitting instrumentation, energy, texture and instrumental/non-vocal treatment by default. Preserve an explicit no-music request or user-supplied music choice; meaningful unscored passages are valid. Do not require a new routine music questionnaire or main-chat instruction. Present the real proposed score in the existing final preview/card for acceptance or revision.

Use actual native music generation or an accessible approved/cleared music source supported by the host. Produce/resolve a ready music asset with duration and provenance. Do not copy demo music, request a named protected score/celebrity imitation, invent clearance, install an external generator or pretend a missing native tool exists. If required music cannot be produced or used, show a native recovery choice instead of silently claiming it was added. Music preparation is not permission to concatenate clips or add captions contrary to the chosen post-scope: subtitle-only retains the existing assembly or individual-clip layout, and an explicit no-edit/no-music choice is respected.

Build a coherent score for the actual edited duration and emotional arc; avoid unrelated random music per shot. Obtain real beat/downbeat/phrase/drop/ending markers from native analysis or observed playback. Use suitable musical accents for hard cuts while protecting complete words, action and dramatic holds. Adjust music sections/allowed musical tails before forcing any picture change; never accelerate speech or invent analyzed BPM. Audio fades/ducking can smooth score joins without adding visual crossfades. If narrative speech/effects and a beat conflict, preserve their meaning and use a different suitable musical accent.

## Visible native tracks and mix

Read the actual native editor schema/draft and keep each role on genuinely distinct editable tracks. Suggested labels below are human labels, not API types or reserved IDs:

| Track role | Content and required check |
|---|---|
| Picture / Video | Approved prepared clips, source in/out and hard-cut positions; no hidden baked-in model score |
| Speech / Dialogue and Narration | Correct role/narrator audio with timing and voice versions; retain a correct embedded source voice or use dedicated speech tracks, never double both |
| Background music / Background Music | Final automatically prepared whole-film score only; independently adjustable, with genuine beat markers and speech ducking |
| Subtitles / Subtitles | Editable timed captions only when selected; preserve other approved title/text roles separately |
| Sound effects / Sound Effects | Extracted/retained or newly produced required foley and effects; ambience may use its own native track; linked cue timing follows the picture |

Do not flatten the editable draft into one mixed video. Separate tracks must contain actual supported media/cues, not empty placeholders that only look correct. When speech/effects were embedded in the approved prepared clips, use supported native extraction/separation to populate sound tracks where required and disable duplicate embedded playback only AFTER the replacement tracks are verified. Extraction of a mixed soundtrack alone is not isolation of speech versus effects. If the requested genuine track separation cannot be achieved, preserve the audible source and report the actual native limitation; do not manufacture stems or mute sound to make the timeline appear separated. A final exported video may be a normal audiovisual mix; the native draft remains editable by role.

Keep source role/timing maps so linked speech and effects move with the picture during trims/ripple edits. Music must not cover speech or essential sound; use actual supported gain, ducking/fades and inspection, without inventing mixer controls or mandatory unsupported loudness targets. Avoid clipping, duplicate audio, accidental mute/solo, disabled export audio and missing cue tails. Inspect the master output as well as individual tracks. A silent/soloed preview or stale render cannot verify the current full mix.

## Final review and export barrier

Show the actual current synchronized preview, identifying music, speech, effects and selected subtitle status. Final native **Final Edit Review** remains **Approve and export / Request changes / Preview again**. Music/effect/subtitle changes go through the existing native **Edit Instructions** card; edit the same project, update cue timing, and obtain approval of the new preview revision. No extra “continue” interaction is needed.

Export the whole edited video only AFTER explicit approval of its current preview/audio/timeline revision. Preparatory shot renders or supported review previews are not final delivery exports. Re-read the draft before export; a changed mix invalidates approval. Await the actual native export, verify real playable picture, complete audible speech/effects, intended final score, selected subtitles and accessible download. If export audio is absent or differs from the approved mix, repair its technical settings and verify again; any content/mix change requires renewed final review. Deliver the real downloadable finished video and actual editable draft when available. Neither a visible timeline, an export toast nor a picture-only file satisfies completion.

## Subtitle-free delivery preserves the soundtrack

For Generate without subtitles, apply `postproduction-options.md`: native assembly and one reviewed/exported film continue, with dialogue/narration, effects, ambience and final music unless excluded. No-subtitle scope is independent of sound. On an existing draft remove only subtitle-role clips/tracks, preserve titles/required in-scene text, and check the actual preview/export has no unintended subtitles and no missing or doubled sound. A changed caption state needs a new final-preview approval, not new auditions or shot generation. Separate approved clips are a different explicit scope; missing editor capability is not repaired by disabling subtitles.
