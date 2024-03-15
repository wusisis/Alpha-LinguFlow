import { Box, Select } from '@mantine/core'
import React from 'react'
import { Controller } from 'react-hook-form'
import { Parameter, PatternInfo } from '@api/linguflow.schemas'
import { usePatternSchema } from '../useSchema'
import { Input } from './Input'
import { NumberComponent } from './Number'
import { ListComponent } from './List'
import { Secret } from './Secret'
import { Dict } from './Dict'
import { Float } from './Float'
import { Boolean } from './Boolean'

export interface SlotTypeComponentProps {
  formPath: string
  slot: Parameter
  disabled?: boolean
  stackIndex?: number
  required?: boolean
}

const BuiltinTypeComponent: { [k: string]: React.FC<SlotTypeComponentProps> } = {
  text: Input,
  list: ListComponent,
  float: Float,
  integer: NumberComponent,
  boolean: Boolean,
  dict: Dict,
  any: Input
}

const ExternalTypeComponent: { [k: string]: React.FC<SlotTypeComponentProps> } = {
  Secret: Secret
}

export const Slot: React.FC<SlotTypeComponentProps> = React.memo(({ formPath, slot, disabled, stackIndex }) => {
  const subFormPath = `${formPath}.slots.${slot.name}`
  const SlotComponent =
    BuiltinTypeComponent[slot.class_name] || ExternalTypeComponent[slot.class_name] || ExternalTypeSelect
  return (
    <SlotComponent
      formPath={subFormPath}
      slot={slot}
      disabled={disabled}
      stackIndex={stackIndex}
      required={slot.default === null}
    />
  )
})

const ExternalTypeSelect: React.FC<SlotTypeComponentProps> = ({ formPath, slot, disabled, stackIndex