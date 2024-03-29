import ReactJson from 'react-json-view'
import { ApplicationRunInputAnyOf } from '@api/linguflow.schemas'
import { ActionIcon, Group, Textarea, Tooltip } from '@mantine/core'
import { IconSwitchHorizontal } from '@tabler/icons-react'
import { useState } from 'react'
import type { InteractionProps } from '.'

export const ObjectIntercation: React.FC<InteractionProps<ApplicationRunInputAnyOf>> = (props) => {
  const {