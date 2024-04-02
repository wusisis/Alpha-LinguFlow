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
  const inputBlock = (ver.configuration as Config).nodes
    .map((n) => blockMap[n.name])
    .find((n) => INPUT_NAMES.includes(n.name))!
  const InteractionComponent = interactionComponents[inputBlock.name]
  const [value, setValue] = useState<any>(InteractionComponent.defaultValue())
  const [interactions, setInteractions] = useState<InteractionInfo[]>([])
  const [currentInteraction, _setCurrentInteraction] = useState<InteractionInfo>()
  const setCurrentInteraction = (int?: InteractionInfo) => {
    _setCurrentInteraction(int)
    onUpdateCurrentInteraction(int)
  }
  const { mutateAsync: runVersion } = useAsyncRunAppVersionApplicationsApplicationIdVersionsVersionIdAsyncRunPost()
  const [isError, setIsError] = useState(false)
  const { data: fetchingIntercation, isLoading: isInteractionLoading } = useGetInteractionInteractionsInteractionIdGet(
    currentInteraction?.id as string,
    {
      query: {
        enabled: !!currentInteraction?.id && !isInteractionFinished(currentInteraction) && !isError,
        refetchInterval: () => {
          if (isInteractionFinished(currentInteraction)) {
            return false
          }
          return 5000
        },
        refetchIntervalInBackground: true,

        onSuccess: (data) => {
          setCurrentInteraction(data.interaction)
          if (!isInteractionFinished(data.interaction)) {
            return
          }
          setValue(InteractionComponent.defaultValue)
          setInteractions((v) => [...v, data.interaction!])
        },
        onError: (error: InteractionErrResponse) => {
          setIsError(true)
          if (error?.response?.data?.node_id) {
            onInteractionError({
              id: error.response.data.node_id,
              msg: error.response.data.message,
              code: error.response.data.code
            })
          }
        }
      }
    }
  )
  const [_isLoading, setIsLoading] = useState(false)
  const isLoading =
    (_isLoading || isInteractionLoading || (!!fetchingIntercation && !isInteractionFinished(currentInteraction))) &&
    !isError

  const runInteraction = async () => {
    setCurrentInteraction(undefined)
    onInteractionError(undefined)
    setIsError(false)
    setIsLoading(true)
    try {
      const interactionRst = await runVersion({ applicationId: app.id, versionId: ver.id, data: { input: value } })
      const debugRst = await getInteractionInteractionsInteractionIdGet(interactionRst.id)
      setCurrentInteraction(debugRst.interaction)

      if (!isInteractionFinished(debugRst.interaction)) {
        return
      }
      setValue(InteractionComponent.defaultValue)
      setInteractions((v) => [...v, debugRst.interaction!])
    } catch (error: any) {
      setIsError(true)
      if (error?.response?.data?.node_id) {
        onInteractionError({
          id: error.response.data.node_id,
          msg: error.response.data.message,
          code: error.response.data.code
        })
      }
    } finally {
      setIsLoading(false)
    }
  }

  const btnRef = useRef(null)

  return (
    <Group h="100%" style={{ flexWrap: 'nowrap' }}>
      <Group align="flex-start" h="100%" style={{ flexGrow: 1, flexWrap: 'nowrap' }}>
        <Title order={6}>Input</Title>
        <Box h="100%" style={{ flexGrow: 1, overflowY: 'auto' }}>
          <InteractionComponent.component
            value={value}
            onChange={setValue}
            onSubmit={() => (btnRef.current as any as { click: () => void }).click()}
            interactions={interactions}
          />
    