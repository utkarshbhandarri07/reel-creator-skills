# Completed-video delivery

The default package applies to an actual finished-video request. Ideas and scripts remain text-only stages. Explicit user choices override these defaults; preserve choices already made in the conversation.

## Captions

Use `captions.py` after timing to produce short readable cues, `web/captions.json`, and `out/Title.srt`. The renderer composites captions onto both stills and final frames. Its caption box spans x=95–915 and y=1470–1628 on a 1080x1920 canvas, leaving margins around platform controls. These are layout defaults, not guaranteed platform safe areas. Reserve that area while staging the scene; inspect faces, labels and actions for overlap. Keep two lines at most and split cues that would require tiny type.

Match the supplied narration text; preserve punctuation and technical notation. Check cues against the audio when playback is available. Script/silence alignment is approximate: disclose that limitation and never claim exact word timing. When hand-correcting timing, update the JSON and SRT together before rendering. Do not resume stale frames after changing captions.

“No captions” disables both the burned-in captions and SRT. “Video only” omits separate SRT delivery while retaining the default burned-in captions unless the user also disables them. “No music” removes music only; “no background” removes music and SFX.

## Cover

Generate a matching portrait 9:16 cover using the available imagegen skill and tool. Use an inspected representative frame as a style reference, a short topic title, one clear educational graphic, and the established palette and character design. Avoid claims that contradict the actual video length or content. Keep essential copy inset and readable at phone size. Inspect spelling, numbers, algorithm/scientific accuracy, arrows, character consistency and composition. Save the selected image to `out/Title-cover.png`; do not leave it only in the image generator's default folder. If unavailable, report the cover as incomplete without blocking delivery of the finished video. Do not set up or spend through a paid provider as a fallback.

## Posting caption and final files

Write a concise topic-specific social caption: a useful opening hook, a short accurate explanation, optional save/share invitation, and a small relevant hashtag set. Avoid unsupported performance promises and keyword stuffing. Save the final text as `out/Title-posting-caption.txt` and provide the text in chat when helpful.

Deliver the latest MP4, cover, SRT and posting-caption text with clickable absolute local file links and copyable exact absolute paths. Preserve older video versions and clearly identify which has the latest audio. A final check must cover 9:16 dimensions, 30 fps, limited-range yuv420p H.264/AAC, duration, caption layout and the full-duration review sheet. Separate automated checks, sampled-frame inspection and full playback review; only claim what was performed.

For “video only,” skip cover generation and posting-caption writing, and omit the separate subtitle file from delivery. A cover-only or caption-only follow-up operates on the existing video and does not start a new film production.
