import { Button, Group, Text } from '@mantine/core'
import { usePagination } from '@mantine/hooks'
import { IconArrowLeft, IconArrowRight } from '@tabler/icons-react'

export const Pagination: React.FC<{ total: number; page: number; onChange: (page: number) => void }> = ({
  total,
  page,
  onChange
}) => {
  const pagination = usePagination({ total, page, onChange })

  return (
    <Group justify="center">
      <Button
        leftSection={<IconArrowLeft size={16} />}
        variant="light"
        color="gray"
        disabled={pagination.active === 1}
        onClick={() => pagination.previous()}
      >
        Prev
      </Button>
      <Text>
        