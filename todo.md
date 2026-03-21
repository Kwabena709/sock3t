# HolyScreen - Project TODO

## Phase 2: Setup & Design System
- [x] Database schema (songs, annotations, playlists, service history, settings, overlays)
- [x] Global CSS design system (dark theme, church-grade typography, gold accent palette)
- [x] App layout with collapsible sidebar navigation
- [x] Online/offline status indicator in sidebar

## Phase 3: Bible Engine
- [x] Bible version selector dropdown (KJV, WEB, BBE, OEB, and more)
- [x] Online Bible API integration (bible-api.com)
- [x] Offline fallback when API is unavailable
- [x] Bible search by book/chapter/verse or text query
- [x] Bible verse display with annotations and highlighting
- [x] Voice search for Bible verses (Web Speech API)
- [x] Present verse to output screens
- [x] Service history tracking on verse presentation

## Phase 4: Song Lyrics Engine
- [x] Online lyrics search integration (lyrics.ovh API)
- [x] Offline saved songs database
- [x] Song save/delete functionality
- [x] Song annotations and highlighting
- [x] Song display with slide management
- [x] Present song to output screens
- [x] Service history tracking on song presentation

## Phase 5: Multi-Screen Output System
- [x] Operator view (full control panel)
- [x] Stage view (performer monitor)
- [x] Audience view (clean presentation output)
- [x] Preacher view (notes + reference)
- [x] Output lock/unlock per screen (global + individual)
- [x] Slide navigation controls (prev/next)
- [x] Clear all outputs
- [x] Open fullscreen output window

## Phase 6: Overlays, Timers & Calendar
- [x] Premium overlay templates (lower thirds, full-screen, corner, ticker)
- [x] Countdown timer with alarm
- [x] Count-up timer (stopwatch)
- [x] Live clock/time display
- [x] Calendar widget
- [x] Overlay customization (color, font, opacity, animation)
- [x] Overlay activation/deactivation

## Phase 7: Settings, History & CCLI
- [x] Settings panel (church name, Bible version, display preferences)
- [x] Service history tracking
- [x] Playlist management (create, edit, reorder, delete)
- [x] CCLI reporting (song usage log with date range filter)
- [x] User preferences persistence (database-backed)

## Phase 8: Polish & Advanced Features
- [x] Voice-to-text search (Web Speech API)
- [x] NDI output info panel and configuration guide
- [x] Premium overlay animations (slide-up, fade-in)
- [x] Dashboard with live clock and quick access
- [x] Online/offline graceful fallback
- [x] Comprehensive vitest test suite (28 tests, all passing)
- [x] TypeScript strict mode (0 errors)

## Future Updates (v2.0+)
- [ ] Keyboard shortcuts for presentation control
- [ ] Import/export playlists and songs (JSON/CSV)
- [ ] Mobile-responsive operator view
- [ ] Real NDI SDK integration (requires native desktop wrapper)
- [ ] Electron/Tauri packaging for true desktop app
- [ ] Background image/video support for slides
- [ ] Multi-language Bible support
- [ ] Cloud sync for settings and playlists
- [ ] MIDI controller support for slide navigation
- [ ] Chord charts display for musicians

## v1.1 Updates
- [x] Rename app from "HolyScreen" to "HolyScreen" across all files
- [x] Build theme selection UI in Settings (scrollable color skin picker)
- [x] Create 12 color themes (Deep Space, Royal Purple, Forest Green, Ocean Blue, Crimson Red, Amber Gold, Rose Pink, Slate Gray, Midnight Teal, Copper Bronze, Ice White, Holy Fire)
- [x] Persist selected theme to database settings
- [x] Apply theme CSS variables globally on theme change
- [x] Theme context provider to share active theme across all components

## v1.2 Updates
- [x] Remove annotation system completely from BiblePage (UI, state, trpc calls)
- [x] Remove annotation system completely from SongsPage (UI, state, trpc calls)
- [x] Remove annotation tRPC router procedures from server/routers.ts
- [x] Drop annotations table from database schema (table retained in DB but unused — safe to drop manually if desired)

## v1.3 Updates
- [x] Replace ALL "Church Presenter" references with "HolyScreen" across every file
## v1.4 Updates — Remote Control
- [x] WebSocket server for real-time remote control sync
- [x] Remote Control page with QR code pairing and session PIN
- [x] Mobile-optimized /remote interface (works on any device)
- [x] Slide prev/next navigation from remote
- [x] Clear/blank all screens from remote
- [x] Lock/unlock output from remote
- [x] Timer start/stop/reset from remote
- [x] Current slide preview on remote device
- [x] Remote Control sidebar nav item
- [x] Wire remote commands into Output, Bible, Songs, Timers pages

## v1.5 Updates — Output Screen Consistency Fix
- [x] Audit all four output screen display panels for size and layout inconsistencies
- [x] Standardize Audience screen — large, clean, centered text optimized for projector
- [x] Standardize Preacher screen — readable reference format with verse context
- [x] Standardize Stage screen — lyrics with song structure labels, chord-friendly layout
- [x] Standardize Operator screen — full controls with next-slide preview panel
- [x] Ensure all four screens use consistent card sizing and proportional font scaling
- [x] Add screen-type labels and purpose descriptions to each panel header

## v1.6 Updates — Vite HMR Fix
- [x] Fix Vite HMR WebSocket configuration for proxied sandbox environment

## v2.1 Updates — Offline Bible Engine
- [x] Bundle KJV Bible JSON as static server-side data (no external API dependency)
- [x] Create offline Bible tRPC router (search, getPassage, getBooks, getChapter, listVersions)
- [x] Unified version dropdown: KJV, NIV, NKJV, AMP, WEB, MSG, TWI, ESV, NASB, NLT, CSB, RSV
- [x] Online/offline source toggle on Bible page
- [x] Auto-fallback to offline KJV when internet is unavailable
- [x] Both online and offline share the same version dropdown UI
- [x] Offline availability badge per version in dropdown
- [x] Browse KJV by book and chapter (OT/NT sections)
- [x] 32 vitest tests passing (7 new offline Bible tests)
## v2.1.1 Bug Fixes
- [x] Fix offline search/passage queries firing with empty string on mount (validation error)
- [x] Fix Vite HMR WebSocket failing in proxied sandbox (clientPort/protocol merged into middlewareMode options)

## v2.2 Updates — ProPresenter-style Media Section
- [x] Add media_categories and media_items tables to database schema
- [x] Build server tRPC router: createCategory, listCategories, deleteCategory, uploadMedia, listMedia, deleteMedia
- [x] S3 upload for images, videos, audio files
- [x] MediaPage: left sidebar with category/playlist list (create, rename, delete)
- [x] MediaPage: main thumbnail grid with hover play overlay
- [x] MediaPage: file type badges (IMG/VID/AUD) and video duration display
- [x] MediaPage: click to send as Background layer
- [x] MediaPage: button to send as Foreground layer
- [x] MediaPage: Clear Background and Clear Foreground buttons
- [x] MediaPage: loop toggle and transition selector (Cut/Dissolve/Fade)
- [x] MediaPage: currently-playing bottom bar with playback controls
- [x] MediaPage: audio playlist panel with play/pause/volume/loop
- [x] Output screens: show active background media behind slide text
- [x] Remove Overlays page and nav item
- [x] Remove Bible page and nav item (code retained for future rebuild)
- [x] Update App.tsx routing
- [x] 32 vitest tests passing (all passing after v2.2 changes)

## v2.3 Updates — Timer Output Integration
- [x] Add "Present Timer" button to TimersPage (countdown, count-up, clock)
- [x] Write live timer state to localStorage (cp_timer_output) every second when presenting
- [x] Add "Clear Timer from Screen" button on TimersPage
- [x] Update Audience screen to read and render live timer in large text
- [x] Timer label shown alongside the time value on output screens
- [x] Timer stops showing on output when cleared or timer is stopped
- [x] Green "Live on Output Screens" badge shown when timer is presenting
- [x] 32 vitest tests passing, 0 TypeScript errors

## v2.3.1 Bug Fixes — Timer Output
- [x] Fix timer freeze/stacking on output screen (decouple React state from localStorage writes)
- [x] Add screen-target selector: operator chooses Audience, Stage, Preacher, or any combination
- [x] Timer output respects selected screens — only renders on chosen screens
- [x] Screen selector shown as checkboxes before "Send to Screen" button
- [x] 32 vitest tests passing, 0 TypeScript errors
