
import React, { useMemo, useState } from 'react'
import {
  ActionIcon,
  Anchor,
  Avatar,
  Badge,
  Button,
  Card,
  Code,
  Container,
  Divider,
  Group,
  Input,
  Loader,
  Menu,
  Modal,
  Skeleton,
  Stack,
  Text,
  Title,
  useMantineTheme
} from '@mantine/core'
import { IconApps, IconDots, IconRocket, IconSearch, IconTrash } from '@tabler/icons-react'
import { Link, useParams } from 'react-router-dom'
import {
  getListAppVersionsApplicationsApplicationIdVersionsGetQueryKey,
  useDeleteAppVersionApplicationsApplicationIdVersionsVersionIdDelete,
  useGetAppApplicationsApplicationIdGet,
  useListAppVersionsApplicationsApplicationIdVersionsGet
} from '@api/linguflow'
import { ApplicationInfo, ApplicationVersionInfo } from '@api/linguflow.schemas'
import { useQueryClient } from 'react-query'
import { useDisclosure } from '@mantine/hooks'
import { Pagination } from '../../components/Pagination'

import { NoResult } from '../../components/NoResult'
import { Layout } from '../../components/Layout/Layout'
import { PublishModal } from '../shared/PublishModal'
import classes from './index.module.css'
import { getDateTime } from './utils'
import { VersionListHeader } from './Header'

const PAGE_SIZE = 12

export const VersionList: React.FC = () => {
  const theme = useMantineTheme()
  const { appId } = useParams()
  const { data: appData, isLoading: appLoading } = useGetAppApplicationsApplicationIdGet(appId!)
  const { data: versionData, isLoading: versionLoading } = useListAppVersionsApplicationsApplicationIdVersionsGet(
    appId!
  )
  const app = appData?.application
  const versions = versionData?.versions
  const [search, setSearch] = useState('')
  const [page, setPage] = useState(1)
  const totalPage = Math.ceil((versions?.length || 0) / PAGE_SIZE)
  const searchedVersions = useMemo(
    () =>
      search
        ? versions?.filter(
            (v) =>
              v.id.toLowerCase().includes(search.toLowerCase()) || v.name.toLowerCase().includes(search.toLowerCase())
          )
        : versions,
    [versions, search]
  )
  const displayedVersions = useMemo(
    () => searchedVersions?.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE),
    [searchedVersions, page]
  )
  const [isPublishing, setIsPublishing] = useState(false)

  return (
    <Layout
      header={{
        height: app?.active_version ? 213 : 184,
        withBorder: false,
        bottomSection: (
          <VersionListHeader app={app} versions={versions} appLoading={appLoading} isPublishing={isPublishing} />
        )
      }}
    >
      <Stack mih="100vh" gap={0} align="stretch">
        <Container size="lg" py="xl" w="100%">
          <Stack>
            {(versionLoading || !!versions?.length) && (
              <Group justify="space-between">
                <Input
                  className={classes.search_input}
                  leftSection={appLoading ? <Loader color="gray" size={14} /> : <IconSearch size={16} />}
                  placeholder="Search versions"
                  disabled={appLoading || versionLoading}
                  value={search}
                  onChange={(e) => setSearch(e.currentTarget.value)}
                />
              </Group>
            )}

            {versionLoading && <LoadingList />}
            {!versionLoading && !!displayedVersions?.length && (
              <List
                app={app!}
                versions={displayedVersions}
                onPublish={() => setIsPublishing(true)}
                onPublished={() => setIsPublishing(false)}
              />
            )}
            {!versionLoading && !versions?.length && (
              <Stack align="center">
                <Avatar size="lg" radius="sm" variant="default">
                  <IconApps size="2rem" color={theme.colors.gray[6]} />
                </Avatar>
                <Text c="gray.7" fz="sm">
                  Create your first version
                </Text>
              </Stack>
            )}
            {!versionLoading && !displayedVersions?.length && !!versions?.length && <NoResult />}

            {!versionLoading && (searchedVersions?.length || 0) > PAGE_SIZE && (
              <Pagination page={page} onChange={setPage} total={totalPage} />
            )}
          </Stack>
        </Container>
      </Stack>
    </Layout>
  )
}

const LIST_ITEM_HEIGHT = 86

const List: React.FC<{
  app: ApplicationInfo
  versions: ApplicationVersionInfo[]
  onPublish: (v: string) => void
  onPublished: () => void
}> = ({ app, versions, onPublished, onPublish }) => {
  const [publishingId, setPublishingId] = useState('')

  return (
    <Card withBorder p={0}>
      {versions.map((v, i) => {
        const isPublished = app?.active_version === v.id
        return (
          <React.Fragment key={v.id}>
            <VersionItem
              ver={v}
              isPublished={isPublished}
              publishingId={publishingId}
              setPublishingId={setPublishingId}
              onPublish={onPublish}
              onPublished={onPublished}
            />
            {i !== versions.length - 1 && <Divider color="gray.3" />}
          </React.Fragment>
        )
      })}
    </Card>
  )
}

const VersionItem: React.FC<{
  ver: ApplicationVersionInfo
  isPublished: boolean
  publishingId: string
  setPublishingId: (id: string) => void
  onPublish: (v: string) => void
  onPublished: () => void
}> = ({ ver, isPublished, publishingId, setPublishingId, onPublish, onPublished }) => {
  const [publishModalOpened, { open: openPublishModal, close: closePublishModal }] = useDisclosure(false)

  return (
    <Group p="md" justify="space-between" h={LIST_ITEM_HEIGHT}>
      <Stack gap={4} w="60%">
        <Group gap="xs" wrap="nowrap">
          <Anchor component={Link} to={`./ver/${ver.id}`} maw="80%" lineClamp={1} underline="never" c="dark">
            <Title order={5}>{ver.name}</Title>
          </Anchor>
          {!!publishingId && ver.id === publishingId && (
            <Badge color="orange" radius="sm" variant="light">
              Publishing...
            </Badge>
          )}
          {isPublished && (
            <Badge color="blue" radius="sm" variant="light">
              Published
            </Badge>
          )}
        </Group>
        <Text c="gray.7" fz="sm" truncate>
          Ver.{' '}
          <Text span fz="xs" style={{ fontFamily: 'monospace' }}>
            {ver.id}
          </Text>
        </Text>
      </Stack>

      <Group>
        <Stack gap={4} align="flex-end" c="gray.7" fz="sm">
          <Text>{getDateTime(ver.created_at)}</Text>
          <Text>by {ver.user}</Text>
        </Stack>
        <Menu shadow="md" width={140} withinPortal position="bottom-end" keepMounted>
          <Menu.Target>
            <ActionIcon variant="subtle" color="gray" size="sm" onClick={(e) => e.stopPropagation()}>
              <IconDots size={16} />
            </ActionIcon>
          </Menu.Target>

          <Menu.Dropdown onClick={(e) => e.stopPropagation()}>
            <Menu.Item leftSection={<IconRocket size={14} />} disabled={isPublished} onClick={openPublishModal}>
              Publish
            </Menu.Item>
            <PublishModal
              ver={ver}
              opened={publishModalOpened}
              close={closePublishModal}
              beforePublish={() => {
                setPublishingId(ver.id)
                onPublish(ver.id)
              }}
              onSuccess={() => {
                setPublishingId('')
                onPublished()
              }}
            />
            <Menu.Divider />

            <DeleteVersionButton ver={ver} disabled={isPublished} />
          </Menu.Dropdown>
        </Menu>
      </Group>
    </Group>
  )
}

const LoadingList: React.FC = () => {
  return (
    <Card withBorder p={0}>
      {Array(PAGE_SIZE)
        .fill(0)
        .map((_, i) => (
          <React.Fragment key={i}>
            <Group p="md" justify="space-between" h={LIST_ITEM_HEIGHT}>
              <Stack w="35%">
                <Skeleton height={12} />
                <Skeleton height={12} width="70%" />
              </Stack>
              <Skeleton height={12} width="25%" />
            </Group>
            {i !== PAGE_SIZE - 1 && <Divider color="gray.3" />}
          </React.Fragment>
        ))}
    </Card>
  )
}

const DeleteVersionButton: React.FC<{ ver: ApplicationVersionInfo; disabled?: boolean }> = ({ ver, disabled }) => {
  const queryClient = useQueryClient()
  const { mutateAsync, isLoading } = useDeleteAppVersionApplicationsApplicationIdVersionsVersionIdDelete({
    mutation: {
      onSuccess: () =>
        queryClient.fetchQuery({ queryKey: getListAppVersionsApplicationsApplicationIdVersionsGetQueryKey(ver.app_id) })
    }
  })
  const [opened, { open, close }] = useDisclosure(false)

  return (
    <>
      <Modal
        closeOnClickOutside={!isLoading}
        closeOnEscape={!isLoading}
        withCloseButton={!isLoading}
        opened={opened}
        onClose={close}
        title={
          <Text fw="bold">
            Delete <Code fz="md">{ver.name}</Code>
          </Text>
        }
        centered
      >
        <Text size="sm">Deleting the app version may cause online malfunctions. Confirm to delete the version?</Text>

        <Group mt="xl" justify="end">
          <Button variant="default" onClick={close} disabled={isLoading}>
            Cancel
          </Button>
          <Button
            color="dark"
            loading={isLoading}
            onClick={async () => {
              await mutateAsync({ applicationId: ver.app_id, versionId: ver.id })
              close()
            }}
          >
            I understand, delete it.
          </Button>
        </Group>
      </Modal>

      <Menu.Item disabled={disabled} color="red" leftSection={<IconTrash size={14} />} onClick={open}>
        Delete
      </Menu.Item>
    </>
  )
}