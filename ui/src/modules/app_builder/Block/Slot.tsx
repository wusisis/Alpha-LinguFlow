import { Box, Select } from '@mantine/core'
import React from 'react'
import { Controller } from 'react-hook-form'
import { Parameter, PatternInfo } from '@api/linguflow.schemas'
import { usePatternSchema } from '../useSchema'
import { Input } from './Input'
import { NumberComponent } from './Number'
import { ListComponent } from './List