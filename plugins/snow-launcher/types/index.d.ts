export type LauncherSkill = { label: string; skill: string }

declare module 'claude-code' {
  interface PluginState {
    'snow-launcher': { isOpen: boolean }
  }
}
