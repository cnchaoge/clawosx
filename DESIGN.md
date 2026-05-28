# ClawOSX Config Tool — Design Specification

## 1. Concept & Vision

A clean, trustworthy configuration tool for a USB-portable AI assistant. The UI should feel like a well-crafted utility — calm, organized, and approachable for non-technical users. Think "system settings panel" not "marketing page." No dark theme, no gradients, no decoration for decoration's sake. Every pixel serves clarity.

---

## 2. Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Background | `#F4F6F9` | App background — warm off-white |
| Card | `#FFFFFF` | Section cards with border |
| Primary | `#2563EB` | Buttons, active labels |
| Primary Hover | `#1D4ED8` | Button hover |
| Success | `#16A34A` | Running status, start button |
| Danger | `#DC2626` | Stop button |
| Warning | `#D97706` | Loading state |
| Text Primary | `#111827` | Headings, main labels |
| Text Secondary | `#6B7280` | Hints, secondary labels |
| Border | `#E2E8F0` | Card borders, dividers |
| Input Background | `#F8FAFC` | Entry field fill |
| Input Focus | `#EFF6FF` | Entry on focus (blue tint) |
| Inner Background | `#F8FAFC` | Channel sub-sections |
| Disabled | `#D1D5DB` | Inactive toggle track |

### Status Dot Colors
- Running → `#16A34A` (green)
- Stopped → `#9CA3AF` (gray)
- Loading → `#D97706` (amber)

---

## 3. Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| App title | Microsoft YaHei UI | 24px | Bold |
| App subtitle | Microsoft YaHei UI | 10px | Regular |
| Section title | Microsoft YaHei UI | 9px | Bold, uppercase accent |
| Field label | Microsoft YaHei UI | 9px | Regular |
| Entry text | Microsoft YaHei UI | 10px | Regular |
| Button | Microsoft YaHei UI | 10px | Bold |
| Status label | Microsoft YaHei UI | 10px | Medium |
| Footer | Microsoft YaHei UI | 8px | Regular |

---

## 4. Layout & Structure

### Window
- Size: `560 × 820` px, minimum `500 × 720`
- Background: `#F4F6F9`
- Scrollable canvas with vertical scrollbar

### Vertical Rhythm (top → bottom)
1. **Header** — App name + version tag (no card)
2. **Status Card** — Service state + action buttons + Begin Chat
3. **AI Config Card** — Provider selection + API Key + Model
4. **Channels Card** — Feishu section + Telegram section
5. **Footer** — Portable storage note

### Card Structure
- `padx=20`, `pady=16` outer padding
- Card border: `relief="solid"`, `bd=1`, color `#E2E8F0`
- Card gap: `5px` vertical between cards
- Section titles inside card: left-border-accent style (3px blue bar)

---

## 5. Component Specifications

### 5a. Status Card
- **Status dot**: Canvas-drawn oval (14×14px), true circle via create_oval
- **Begin Chat button**: Full-width, `#16A34A` bg, 12px Bold, `pady=8`
- **Refresh button**: `#E2E8F0` bg, `#111827` text

### 5b. AI Config Card
- **Provider pills**: Frame-based clickable pills, selected = `#EFF6FF` bg + left blue border
- **Entry fields**: flat relief, focus = groove ring in primary blue
- Focus ring: `highlightthickness=1`, `highlightcolor="#2563EB"`

### 5c. Channel Cards
- Each channel in a sub-card with inset background `#F8FAFC`
- **Enable toggle**: Pill-style track (36×20px) + oval thumb (14×14px white)
  - On: `#2563EB` track, thumb at right
  - Off: `#D1D5DB` track, thumb at left
- **Save button**: Primary blue `#2563EB`, centered

### 5d. Button Hover Effects
All buttons have hover/leave color restoration:
- Primary: `#1D4ED8`
- Success: `#147a3e`
- Danger: `#b91c1c`
- Gray: `#c4c9d1`

### 5e. Input Focus States
- `<FocusIn>`: bg → `#EFF6FF`, relief → `groove`
- `<FocusOut>`: bg → `#F8FAFC`, relief → `flat`

---

## 6. Spacing System

```
Window horizontal padding:   20px
Card padding:                20px horizontal, 16px top/bottom
Card gap (between cards):    5px vertical
Section title padding:        14px top, 8px bottom
Internal section gap:         8px
Field-to-field gap:           6px
Button gap (adjacent):        6px
Sub-card indent:              12px horizontal
```

---

## 7. Specific Visual Improvements Implemented

- [x] Status dot — Canvas-drawn true oval, color-coded by state
- [x] Provider pills — Frame-based clickable tabs, selected state highlighted
- [x] Pill toggle for channel enable — Track + oval thumb, primary blue when on
- [x] Section title — Left border accent (3px blue bar)
- [x] Card borders — `relief="solid"`, visible on any background
- [x] Input focus states — Blue tint bg + groove ring on focus
- [x] Button hover effects — All buttons darken on hover
- [x] Scrollable canvas — Handles window too small to show all content