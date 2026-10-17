import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

// Ajouter une ligne ici = un nouveau bouton. `skill` = nom affiché par /skills.
const SKILLS = [
  { label: 'Besoin', skill: 'servicenow-techlead-toolkit:requirement-shaper' },
  { label: 'Conception', skill: 'servicenow-techlead-toolkit:solution-design' },
  { label: 'CSDM', skill: 'servicenow-techlead-toolkit:csdm-assistant' },
  { label: 'Chiffrage', skill: 'servicenow-techlead-toolkit:chiffrage-rapide' },
  { label: 'Revue code', skill: 'servicenow-techlead-toolkit:code-review' },
  { label: 'Sécurité', skill: 'servicenow-techlead-toolkit:security-review' },
  { label: 'Tests ATF', skill: 'servicenow-techlead-toolkit:atf-test-generator' },
  { label: 'Comms', skill: 'servicenow-techlead-toolkit:communication' },
] as const

const isOpen = atom({ plugin: 'snow-launcher', key: 'isOpen' } as const, true)

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'snow', description: 'Afficher ou masquer la barre ServiceNow' })
    return next(e)
  })

  on('command.run', { command: 'snow' }, async $ => {
    await update($, isOpen, v => !v)
    return { text: 'Barre ServiceNow basculée.' }
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey || !(await read($, isOpen))) return next(e)
    const { Box, Button, Text } = $.ui.resolve(e)
    return (
      <Box>
        <Text dimColor>SNOW </Text>
        {SKILLS.map(s => (
          <Button
            key={s.skill}
            label={s.label}
            onPress={() => void $.prompt.fill({ text: `/${s.skill} `, mode: 'replace' })}
          />
        ))}
      </Box>
    )
  })
}
