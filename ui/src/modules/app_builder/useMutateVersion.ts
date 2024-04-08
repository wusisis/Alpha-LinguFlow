import {
  useCreateAppVersionApplicationsApplicationIdVersionsPost,
  useUpdateAppVersionMetaApplicationsApplicationIdVersionsVersionIdPut
} from '@api/linguflow'
import { useNavigate, useParams } from 'react-router-dom'
import { useReactFlow } from 'reactflow'
import { useFormContext } from 'react-hook-form'
import dayjs from 'dayjs'
import { ApplicationVersionInfo } from '@api/linguflow.schemas'
import { useEffect, useState } from 'react'
import { useGetLinguFlowEdge } from './Block/useValidConnection'

export const getCurrentDateTimeName = () => `v${dayjs().format('YYYY-MM-DD')}.${dayjs().unix()}`

export const useCreateVersion = (version?: ApplicationVersionInfo) => {
  const { appId, verId } = useParams()
  const navigate = useNavigate()
  const { getNodes } = useReactFlow()
  const getLinguFlowEdge = useGetLinguFlowEdge()
  const { getValues, resetField } = useFormContext()
  const { mutateAsync: _createVersion, isLoading } = useCreateAppVersionApplicationsApplicationIdVersionsPost()

  const [canSave, setCanSave] = useState(false)
  const createVersion = async (force = false) => {
    if ((!canSave || isLoading) && !force) {
      return
    }
    setCanSave(false)

    const { id } = await _createVersion({
      applicationId: appId!,
      data: {
        parentId: verId,
        name: getCurrentDateTimeName(),
        configuration: {
          nodes: Object.values(getValues()),
          edges: getLinguFlowEdge()
        },
        metadata: {
          ...version?.metadata,
          ui: {
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            nodes: getNodes().map(({ data, ...n }) => n)
          }
        }
      }
    })

    Object.keys(getValues()