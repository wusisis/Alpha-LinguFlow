import { Anchor, Box, Button, Chip, Code, Divider, Group, Modal, Stack, Text, TextInput, Title } from '@mantine/core'
import { getHotkeyHandler } from '@mantine/hooks'
import {
  getListAppApplicationsGetQueryKey,
  useCreateAppApplicationsPost,
  useUpdateAppMetaApplicationsApplicationIdPut
} from '@api/linguflow'
import { ApplicationInfo } from '@api/linguflow.schemas'
import { useEffect, useState } from 'react'
import { useQueryClient } from 'react-query'
import { useNavigate } from 'react-router-dom'

export interface ModifyAppModelProps {
  opened: boolean
  onClose: () => void
  app?: ApplicationInfo
}

export const ModifyAppModel: React.FC<ModifyAppModelProps> = ({ opened, onClose, app }) => {
  const queryClient = useQueryClient()
  const navigate = useNavigate()
  const [name, setName] = useState(app?.name || '')
  const [langfusePK, setLangfusePK] = useState(app?.langfuse_