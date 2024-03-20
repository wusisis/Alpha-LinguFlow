import { Connection, Node, useReactFlow, useStoreApi } from 'reactflow'
import { useCallback } from 'react'
import { GraphEdge } from '@api/linguflow.schemas'
import { usePatternSchema } from '../useSchema'
import { BlockNodeProps } from '.'

export const BLOCK_PORT_ID_NULL = '__null__'
export const BOOLEAN_CLASS_NAME = 'boolean'

export const useValidConnection = () => {