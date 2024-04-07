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
  onInte