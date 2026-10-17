# Article audio editions

## Current boundary

Audio is prepared infrastructure, not a published show. `_data/audio.json` has no episodes. Do not display inactive players, invented distribution links, an empty podcast feed, or claim that narration has been generated. Apple Podcasts is the podcast destination, not Apple Music.

Mihai approved one stock-voice pilot up to US$5 on 17 October 2026. No recurring generation, voice cloning, paid hosting, or subscriptions are authorized. Credentials must be supplied securely outside tracked files and chat. Do not search sibling company repositories for them. An initial listening sample must be approved before a full rollout.

## Preparation and generation

Choose a published English article with a useful business question. Adapt it for listening: turn tables, code, and equations into faithful spoken explanations; preserve limitations and clearly identify an abridgment. Keep the original citations on the article, and include a full spoken transcript with the eventual episode. Never feed raw Markdown indiscriminately to text-to-speech.

The first sample script is `docs/narration-pilot.txt`. Prepare it without network access:

```sh
python3 scripts/prepare_narration.py _posts/2026-10-17-deep-research-needs-evidence-budget.md docs/narration-pilot.txt
```

This makes model request JSON and source/script hashes in ignored `vendor/narration/`. It neither reads a key nor generates audio. Do not send the request until the script, secure credential access, current price, and remaining pilot budget are checked.

OpenRouter’s [official ElevenLabs instructions](https://openrouter.ai/blog/announcements/elevenlabs-on-openrouter/) document `POST /api/v1/audio/speech`. The prepared request explicitly chooses MP3, a stock voice, and chunks below 9,000 characters. [Current model pricing](https://openrouter.ai/elevenlabs/eleven-v4) was US$40 per million characters under a temporary offer on 17 October, with US$80 shown as the undiscounted rate. Recheck before spending; do not build a budget around the promotion. Use a dedicated provider key with a US$5 spending limit. Reserve the cost of every attempt, including uncertain failures, and do not retry automatically.

Listen for pronunciation of names, acronyms, numbers, sentence stress, and distracting delivery. Check seams, clipping, duration, loudness, and the exact transcript. Record who actually listened and when. Automated metadata checks cannot establish listening quality. Keep unreleased samples and generation logs ignored, and never store keys or private account details in the repository.

## Hosting and accounts

Suggested starting point: Spotify for Creators hosting with one audio-edition show. [RSS is available after the first episode](https://support.spotify.com/us/creators/article/finding-and-enabling-your-rss-feed/); Spotify does not automatically submit it to other directories. Enabling RSS exposes its contact email publicly. Obtain Mihai’s choice of a public show contact, show name, artwork, category, and explicit approval before account creation, agreement acceptance, enabling the feed, or submitting a show. No such actions have been completed.

Submit the real validated feed through [Apple Podcasts Connect](https://podcasters.apple.com/support/897-submit-a-show) only with approval. Apple’s [content guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) require prominent synthetic-audio disclosure in the content and metadata. Use that disclosure in the spoken introduction, show/episode description, and site player. Do not impersonate Mihai’s voice. Narration disclosure is distinct from claims about how the prose was written.

## Publish a verified episode

Use the podcast host’s stable, public HTTPS MP3 enclosure, not a signed or expiring URL. Do not commit large audio binaries to Git. First verify playback, feed validation, byte length, media type, duration, transcript, rights, and actual directory URLs.

Each `_data/audio.json` episode needs `article_url`, repository-relative `source`, `source_sha256`, `transcript` under `/assets/transcripts/`, `transcript_sha256`, `audio_url`, `mime_type: audio/mpeg`, measured `bytes` and `duration_seconds`, a matching `duration_label` in M:SS, stock `voice`, `voice_kind: stock`, `listening_reviewed`, and `listening_reviewed_by`. Optional `spotify_url` and `apple_url` must be real episode links, never guessed destinations. The transcript must say “synthetic voice” and match what listeners hear.

The shared article component adds a native player with no autoplay or preloading and links only to verified destinations. There are no tracking embeds. English audio is not silently attached to a Romanian translation. Source or transcript edits invalidate the audio record. Re-render, listen again, and update hashes only after checking the changed audio; never refresh hashes merely to pass.

Run the normal source, build, unit, link, and responsive visual gates before release. A narration adaptation of an existing article is not a new original essay, but it must not be used to publish a new argument outside the article cadence.
