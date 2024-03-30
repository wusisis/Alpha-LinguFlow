import { ActionIcon, Box, Button, Divider, FileButton, Group, Kbd, Stack, Title, Tooltip } from '@mantine/core'
import { IconPackageExport, IconPackageImport } from '@tabler/icons-react'
import { useRef, useState } from 'react'
import download from 'downloadjs'
import yaml from 'js-yaml'
import { ApplicationInfo, ApplicationVersionInfo, InteractionInfo } from '@api/linguflow.schemas'
import {
  getInteractionInteractionsInteractionIdGet,
  useAsyncRunAppVersionApplicationsApplicationIdVersionsVersionIdAsyncRunPost,
  useGetInteractionInteractionsInteractionIdGet
} from '@api/linguflow'
import { useBlockSchema } from '../../useSchema'
import { Config } from '../../linguflow.type'
import { TextIntercation } from './TextInteraction'
import { ObjectIntercation } from './ObjectInteraction'
import { ListIntercation } from './ListInteraction'

export interface InteractionProps<V = any> {
  value: V
  onChange: (v: V) => void
  onSubmit: () => void
  interactions?: InteractionInfo[]
}

const interactionComponents: {
  [k: string]: { component: React.FC<InteractionProps>; defaultValue: (v?: any) => any }
} = {
  Text_Input: { component: TextIntercation, defaultValue: () => '' },
  Dict_Input: { component: ObjectIntercation, defaultValue: () => ({}) },
  List_Input: { component: ListIntercation, defaultValue: (v) => (v as []) || [] }
}

export const INPUT_NAMES = ['Text_Input', 'Dict_Input', 'List_Input']

const isInteractionFinished = (interaction?: InteractionInfo) => !!interaction?.output

export interface ErrorInteraction {
  id: string
  msg: string
  code: string
}

interface InteractionErrResponse {
  response: { data: { node_id: string; message: string; code: string } }
}

export const Debug: React.FC<{
  app: ApplicationInfo
  ver: ApplicationVersionInfo
  onUpdateCurrentInteraction: (interaction?: InteractionInfo) => void
  onInteractionError: (errorInteraction?: ErrorInteraction) => void
}> = ({ app, ver, onUpdateCurrentInteraction, onInteractionError }) => {
  const { blockMap } = useBlockSchema()