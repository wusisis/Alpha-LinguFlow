import React from 'react'
import { ActionIcon, LoadingOverlay, Tabs } from '@mantine/core'
import { IconX } from '@tabler/icons-react'
import { ApplicationInfo, ApplicationVersionInfo, InteractionInfo } from '@api/linguflow.schemas'
import { Debug, ErrorInteraction } from './Debug'
import { AppInfo } from './AppInfo'
import { TOOLBAR_HEIGHT } from '.'

const TAB_HEIGHT = 36

export enum TabValue {
  DEBUG = 'debug',
  APP_INFO = 'app_info'
}

export const Pane: React.FC<{
  tab: TabValue
  setTab: React.Dispatch<React.SetStateAction<TabValue>>
  setToolbarPaneOpened: React.Dispatch<React.SetStateAction<boolean>>
  app?: ApplicationInfo
  ver?: ApplicationVersionInfo
  isCreatingVersion: boolean
  onUpdateCurrentInteraction: (interaction?: InteractionInfo) => void
  onInteractionError: (errorInteraction?: ErrorInteraction) => void
}> = ({
  tab,
  setTab,
  setToolbarPaneOpened,
  app,
  ver,
  isCreatingVersion,
  onUpdateCurrentInteraction,
  onInteractionError
}) => {
  return (
    <Tabs
      value={tab}
      onChange={(t) => setTab(t as TabValue)}
      variant="outline"
      color="gray"
      h={`calc(100% - ${TOOLBAR_HEIGHT}px)`}
      radius={0}
      style={(theme) => ({ borderTop: `1px solid ${theme.colors.gray[2]}` })}
      pos="relative"
    >
      <LoadingOverlay
        visible={isCreatingVersion}
        zIndex={1000}
        overlayProps={{ radius: 'sm', blur: 2 }}
        loaderP