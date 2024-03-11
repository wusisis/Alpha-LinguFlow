import { Controller } from 'react-hook-form'
import { Box, Switch } from '@mantine/core'
import type { SlotTypeComponentProps } from './Slot'

export const Boolean: React.FC<SlotTypeComponentProps> = ({ slot, formPath, disabled, required }) => {
  return (
    <Controller
      name={formPath}
      render={({ field: { ref, value, onChange } }) => (
        <Switch
          required={required}
          size="xs"
          ref={ref}
          disabled={disabled}
          labelPosition="lef