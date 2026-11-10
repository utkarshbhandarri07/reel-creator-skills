# Consistent Reel Cartoons covers

Use this design for future covers unless the user requests a different style. Existing covers stay unchanged unless explicitly requested.

## Permanent visual reference

Inspect [the approved Selection Sort cover](../assets/selection-sort-thumbnail-reference.png) with the image viewer before generating. Pass the actual bundled image to imagegen as the primary style reference; resolve it relative to this skill, not a temporary attachment or an old project. It is the user's approved existing cover, bundled unchanged from `Reels/Covers/Selection-Sort-Cover.png`. Use its character, painted finish and visual proportions, not its algorithm content, for new subjects.

## Fixed visual identity

- Portrait 9:16, targeting 1080x1920. Fill the composition with a rounded cream board outlined in dark plum; leave breathing room around essential copy and graphics.
- Upper board: a large, playful, chunky plum topic heading with a restrained dimensional shadow. Put the second title line in cream letters on a teal ribbon. For example: `SELECTION` / `SORT`, `BUBBLE` / `SORT`, `LINEAR` / `SEARCH`. Preserve this hierarchy for longer topics by using a short accurate title or balanced line breaks instead of tiny lettering.
- Place a cream/gold rounded `FOR BEGINNERS` badge outlined in plum immediately below the title, with short teal rules at its sides. Keep the wording unless the user asks otherwise.
- Centre: one clear teaching graphic with generous spacing. For arrays, use rounded cream tiles with plum numbers/outlines, amber and pink emphasis, and clear arrows only where the operation calls for them. Adapt the graphic to the subject; a search must not inherit sorting/swap arrows.
- Under the graphic: one short teal uppercase takeaway, normally 2–5 words. Keep it accurate and action-oriented, such as `FIND MIN → SWAP` or `FIRST MATCH WINS`.
- Lower left: the same cheerful bean-head teacher, dark plum side-swept hair, warm skin, teal collared shirt, plum limbs/outlines, smiling with closed crescent eyes and pointing toward the lesson. Keep the face, silhouette, scale and position consistent; keep the gesture clear of essential content.
- Surroundings: painted blue/teal sky with soft cream clouds, green hills/bushes and a warm wooden stage. Retain the reference's cream/plum/teal palette, amber accents, pink highlight, soft lighting, tactile painted surfaces and bold outlines. Small amber emphasis strokes may frame the title or pointing gesture.

Change the topic words, relevant diagram values/highlights/arrows and takeaway for each lesson. Preserve the visual identity and relative placement. Do not add code panels, dense explanatory paragraphs, video-caption overlays, duration claims, extra characters or new branding by default. A video frame is optional supporting content guidance, not a replacement style reference.

## Generation prompt pattern

Use the imagegen skill and built-in tool. Supply the bundled image as the primary visual reference and label any video frame as a secondary topic reference. A useful prompt is:

> Create a portrait 9:16 educational cover in the same visual identity and composition as the supplied approved cover. Preserve the rounded cream/plum board, chunky plum first title line, cream second title line on a teal ribbon, FOR BEGINNERS badge, painted sky/hills/wood stage, and the same cheerful dark-haired teal-shirt teacher pointing from the lower left. Change only the lesson-specific content: title [FIRST LINE] / [SECOND LINE], central teaching graphic [precise values, labels, highlights and arrows], short teal takeaway [EXACT TEXT]. Keep essential content inset, uncluttered and readable at phone thumbnail size. Follow the actual lesson, including correct indices and operation direction.

Example adaptations for prompt review, not requests to regenerate existing files:

- **Bubble Sort:** `BUBBLE` / `SORT`; tiles `[5, 1, 4, 2]`; highlight adjacent 5 and 1, show their exchange with a clear pair of arrows; takeaway `COMPARE → SWAP`. Do not imply non-adjacent swaps or a fully sorted array after one exchange.
- **Linear Search:** `LINEAR` / `SEARCH`; tiles `[8, 3, 6, 3]`, zero-based labels `[0, 1, 2, 3]`, small `TARGET = 3` label; highlight the first 3 at index 1, with a pointer labelled `RETURN 1`; keep the later 3 neutral; takeaway `FIRST MATCH WINS`. No swap arrows.

## Inspect and save

Inspect the generated image itself, not only its prompt. Check exact spelling, title hierarchy, `FOR BEGINNERS`, values, indices, highlight meaning, arrow direction, and consistency of teacher/palette/composition with the bundled reference. Also inspect a thumbnail-sized view: the title and central teaching point must remain legible. Correct defects with a focused imagegen revision using the same reference.

Save the selected image to the current project's `out/Title-cover.png` and copy the exact same bytes to `C:/Users/utkarsh/Desktop/Development/Reels/Covers/Title-cover.png`. Create that central folder if missing. If either destination already holds different content, choose the next unused `Title-cover-v2.png`, `-v3.png`, etc. available in both folders; never overwrite older versions. An identical existing file may be reused. Verify both copies have the same SHA-256 and provide both absolute paths. On another machine, use a user-supplied Covers path or a `Covers` folder under that machine's reels root rather than creating this user's Windows directory elsewhere. Keep the bundled reference read-only.
