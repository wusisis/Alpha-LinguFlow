import { Controller } from 'react-hook-form'
import { Textarea } from '@mantine/core'
import type { SlotTypeComponentProps } from './Slot'

export const Input: React.FC<SlotTypeComponentProps> = ({ slot, formPath, disabled, required }) => {
  return (
    <Controller
      name={formPath}
      render={({ field: { ref, value, onChange } }) => (
       