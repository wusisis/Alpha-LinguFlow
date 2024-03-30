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
import { ListIntercation } from './ListInte