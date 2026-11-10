---
name: upload-youtube
description: Upload existing videos or Shorts to YouTube Studio through connected Chrome, set titles, descriptions, tags and thumbnails, and save or schedule releases. Use for requested YouTube upload and metadata workflows, including Dinke4Leetcode; video creation belongs to a production skill.
---

# Upload YouTube

Complete the requested YouTube Studio upload or metadata change using existing media. User instructions override these defaults. The skill supplies a workflow, not standing permission to publish future videos.

## Prepare

- Use the connected Chrome browser when requested. Read the browser tool's current documentation and file-upload guidance. Discover live tabs and verify the signed-in channel; never reuse browser or tab IDs from earlier runs without checking them.
- Locate the final MP4, matching cover, and transcript or posting caption. Inspect the content and actual duration before writing metadata; distinguish the latest approved video from earlier versions. Ask only for missing information that affects the upload.
- For this user's work, look under `C:/Users/utkarsh/Desktop/Development/Reels/<topic>/out/`. Prefer the supplied path or current production handoff over filename guesses.
- Check Studio for an existing upload or draft of the same video before starting another. Resume it rather than creating a duplicate.

## Metadata and media

- Draft a concise, accurate title, topic-specific description, relevant hashtags and search tags. Reuse approved wording. A duration in the title must match the actual video length; do not promise ranking or reach.
- For Dinke4Leetcode beginner algorithm videos, prefer **DSA for Beginners** in the title. Keep language-specific implementation details, such as C++, in the description and tags when present in the video. Mention DSA, LLD and HLD in the channel subscription line, without implying every video covers all three.
- Upload the existing matching cover and verify its preview. Do not substitute a generated frame and call it the requested custom cover. Creating a new cover is a separate creative task unless requested.
- For beginner concept explanations, use Education, Concept overview, Beginner, and English when applicable. Leave unrelated playlists, account settings and monetization settings unchanged. Add a related video only when requested and available.
- Set audience, age restriction, paid promotion and AI disclosure from the intended audience and actual production facts using the current questions in Studio. A cartoon alone does not establish a child-directed audience; do not answer disclosure questions from the file style alone.

## No timestamp mapping

- Skip manual chapters, timestamped description sections and the Education **Problems** timecode mapping unless the user explicitly requests them. Keep the Problems field empty for ordinary concept explainers.
- Do not create, map, align or manually edit subtitle timestamps as part of an upload. Preserve captions already burned into the video. An existing SRT may be uploaded unchanged when requested; if that upload is blocked, report it rather than recreating its timings in the editor.
- Do not modify the video, narration, duration, or production skill to satisfy an upload task.

## Visibility and scheduling

- Follow the user's requested public, private, unlisted or scheduled visibility. If unspecified, prepare and save privately, then resolve visibility before publishing. A metadata-only edit does not authorize a visibility change.
- Dinke4Leetcode is the default channel for this user's requests unless another is named; verify the channel in Studio. Use Asia/Kolkata (IST, UTC+05:30) for requested schedules unless the user specifies another zone.
- Apply a 12-hour interval only when requested. Calculate it from the preceding video's actual public release time, not its upload date. If only a date is visible, ask for the time or an explicit approximation; do not silently assume midnight. For multiple uploads, apply the agreed interval successively.
- Display the resulting absolute date, time and zone before saving. If it is already past, request a replacement time. Verify the zone in Studio and that the video remains private until publication.
- Save the authorized release without asking for the same permission again. This skill does not authorize recurring schedules or background monitoring.

## Upload failures and verification gates

- Use supported browser file choosers with absolute local paths. If the extension reports missing file-URL access, follow its documented troubleshooting. If the user must select a file manually, leave the correct control ready and give the exact file path; resume the existing upload after selection.
- Custom thumbnails and related-video links can be gated by channel verification or limits. Read the actual prompt and distinguish verification required, review pending, and upload failure. Leave identity verification to the user and do not promise approval or bypass the gate. Continue independent authorized work and identify unfinished deliverables.
- After each UI change, inspect current state before deciding the next action. Use fresh controls, especially after dialogs close. Do not persist an incomplete caption draft. If a recovery action would remove user-authored work, resolve that explicitly first.
- On saving failures, inspect the error and use a documented retry when appropriate. If the same failure persists, preserve the existing draft and stop retrying that action; do not reload away unsaved work, delete an upload or start a duplicate.

## Verify and deliver

- Confirm processing and copyright-check results without guaranteeing future claim status. Reopen saved details to verify the requested title, description, tags, thumbnail and visibility persisted. For scheduled videos, confirm the saved date, time and zone.
- Save a screenshot of the result beside the media when possible, and embed it in the final reply. Preserve the live page for a required user handoff using the browser's documented mechanism.
- Return the video link, concise saved settings, and any remaining blockers. Distinguish entered, saved, scheduled and public states. Never claim a custom thumbnail or subtitle file was uploaded when only an automatic thumbnail or burned-in captions are present.
- Verify discovery in a later turn's skill catalog before claiming that this newly installed skill has been activated by the host.
