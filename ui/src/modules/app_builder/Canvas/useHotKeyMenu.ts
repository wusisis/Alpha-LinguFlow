import { getHotkeyHandler } from '@mantine/hooks'
import { useEffect, useRef, useState } from 'react'

export const useHotKeyMenu = (toolbarFocusedRef: React.RefObject<boolean>) => {
  const [menuPosition, setMenuPosition] = useState([0, 0])
  const [hotKeyMenuOpened, setHotKeyMenuOpened] = useState(false)
  const menuStatus = useRef({
    inPane: true,
    // init position without mouse event
    mouseX: window.innerWidth / 3,
    mouseY: window.innerHeight / 4
  })

  const onPaneMouseEnter: (event: React.MouseEvent<Element, MouseEvent>) => void = () => {
    menuStatus.current.inPane = true
  }
  const onPaneMouseLeave: (event: React.MouseEvent<Element, MouseEvent>) => void = () => {
    menuStatus.current.inPane = false
  }
  const onPaneMouseMove: (event: React.MouseEvent<Element, MouseEvent>) => void = (e) => {
    menuStatus.current.mouseX = e.clientX
    menuStatus.current.mouseY = e.clientY
  }
  const onNodeMouseEnter: (event: Re