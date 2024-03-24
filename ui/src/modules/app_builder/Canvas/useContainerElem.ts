import { createContext, useContext } from 'react'

const ContainerElemContext = createContext<HTMLDivElement | null>(null)

export const ContainerElem