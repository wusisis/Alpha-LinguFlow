import { Box, DefaultMantineColor, Group, HoverCard, StyleProp, Text, useMantineTheme } from '@mantine/core'
import { IconBug, IconInfoCircle } from '@tabler/icons-react'
import React, { PropsWithChildren, useState } from 'react'

import 'reactflow/dist/style.css'
import { ApplicationInfo, ApplicationVersionInfo, InteractionInfo } from '@api/linguflow.schemas'
import { notifications } from '@mantine/notifications'
import { Config } from '../linguflow.type'
import classes from './index.module.css'
import { Pane, TabValue } from './Pane'
import { ErrorInteraction, INPUT_NAMES } from './Debug'

export const TOOLBAR_HEIGHT = 30
export const TOOLBAR_PANE_HEIGHT = 260

export const Toolbar: React.FC<{
  app?: ApplicationInfo
  ver?: ApplicationVersionInfo
  toolbarPaneOpened: boolean
  setToolbarPaneOpened: React.Dispatch<React.SetStateAction<boolean>>
  isCreatingVersion: boolean
  onUpdateCurrentInteraction: (interaction?: InteractionInfo) => void
  onInteractionError: (errorInteraction?: ErrorInteraction) => void
}> = ({
  app,
  ver,
  toolbarPaneOpened,
  setToolbarPaneOpened,
  isCreatingVersion,
  onUpdateCurrentInteraction,
  onInteractionError
}) => {
  const { colors } = useMantineTheme()
  const [tab, setTab] = useState<TabValue>(TabValue.DEBUG)
  const versionNotSaved = !ver || isCreatingVersion
  const noInputBlock = !((ver?.configuration || {}) as Config)?.nodes?.some((n) => INPUT_NAMES.includes(n.name))

  return (
    <Box h={TOOLBAR_HEIGHT + (toolbarPaneOpened ? TOOLBAR_PANE_HEIGHT : 0)}>
      {toolbarPaneOpened && (
        <Pane
          tab={tab}
          setTab={setTab}
          setToolbarPaneOpened={setToolbarPaneOpened}
          app={app}
          ver={ver}
          isCreatingVersion={isCreatingVersion}
          onUpdateCurrentInteraction={onUpdateCurrentInteraction}
          onInteractionError={onInteractionError}
        />
      )}

      <Group justify="space-between" style={(theme) => ({ borderTop: `1px solid ${theme.colors.gray[1]}` })}>
        <ToolbarButton
          tooltip="Debug"
          bg="gray.2"
          onClick={() => {
            setTab(TabValue.DEBUG)
            if (tab === TabValue.DEBUG || !toolbarPaneOpened) {
              setToolbarPaneOpened((v) => !v)
            }
          }}
          disabled={versionNotSaved || noInputBlock}
  