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
  const [langfusePK, setLangfusePK] = useState(app?.langfuse_public_key || '')
  const [langfuseSK, setLangfuseSK] = useState(app?.langfuse_secret_key || '')
  const [template, setTemplate] = useState<string[]>([])
  const { mutateAsync: createApp, isLoading: isCreating } = useCreateAppApplicationsPost({
    mutation: {
      onSuccess: async (data) => {
        await queryClient.fetchQuery({ queryKey: getListAppApplicationsGetQueryKey() })
        onClose()

        const redirectTo = template.length ? `/app/${data.id}/ver?template=${template[0]}` : `/app/${data.id}`
        navigate(redirectTo)
      }
    }
  })
  const { mutateAsync: updateApp, isLoading: isUpdating } = useUpdateAppMetaApplicationsApplicationIdPut({
    mutation: {
      onSuccess: async () => {
        await queryClient.fetchQuery({ queryKey: getListAppApplicationsGetQueryKey() })
        onClose()
      }
    }
  })
  const handleConfirm = async () => {
    if (isLoading || !opened || !name) {
      return
    }

    if (!app) {
      await createApp({ data: { name, langfusePublicKey: langfusePK, langfuseSecretKey: langfuseSK } })
    } else {
      await updateApp({
        applicationId: app.id,
        data: { name, langfusePublicKey: langfusePK, langfuseSecretKey: langfuseSK }
      })
    }
  }

  const isLoading