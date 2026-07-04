import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { supabase } from '../lib/supabase'
import {
  FALLBACK_MENU_ITEMS,
  FALLBACK_ADDONS,
  FALLBACK_CORN_FLAVORS,
  BRANCHES as FALLBACK_BRANCHES,
} from '../lib/fallbackMenu'

const MenuContext = createContext(null)

export function MenuProvider({ children }) {
  const [state, setState] = useState({
    loading: true,
    usingFallback: false,
    menuItems: [],
    addons: [],
    cornFlavors: [],
    branches: [],
  })

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        const timeout = (ms) => new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), ms))

        const [menuRes, addonsRes, flavorsRes, branchesRes] = await Promise.race([
          Promise.all([
            supabase.from('menu_items').select('*').eq('active', true).order('sort_order'),
            supabase.from('addons').select('*').eq('active', true).order('sort_order'),
            supabase.from('corn_flavors').select('*').eq('active', true).order('sort_order'),
            supabase.from('branches').select('*').eq('active', true).order('sort_order'),
          ]),
          timeout(6000),
        ])

        const hasError = menuRes.error || addonsRes.error || flavorsRes.error || branchesRes.error
        const hasData = menuRes.data?.length && addonsRes.data?.length

        if (cancelled) return

        if (hasError || !hasData) {
          setState({
            loading: false,
            usingFallback: true,
            menuItems: FALLBACK_MENU_ITEMS,
            addons: FALLBACK_ADDONS,
            cornFlavors: FALLBACK_CORN_FLAVORS,
            branches: FALLBACK_BRANCHES,
          })
          return
        }

        setState({
          loading: false,
          usingFallback: false,
          menuItems: menuRes.data,
          addons: addonsRes.data,
          cornFlavors: flavorsRes.data,
          branches: branchesRes.data,
        })
      } catch {
        if (cancelled) return
        setState({
          loading: false,
          usingFallback: true,
          menuItems: FALLBACK_MENU_ITEMS,
          addons: FALLBACK_ADDONS,
          cornFlavors: FALLBACK_CORN_FLAVORS,
          branches: FALLBACK_BRANCHES,
        })
      }
    }

    load()
    return () => {
      cancelled = true
    }
  }, [])

  const value = useMemo(() => state, [state])

  return <MenuContext.Provider value={value}>{children}</MenuContext.Provider>
}

export function useMenu() {
  const ctx = useContext(MenuContext)
  if (!ctx) throw new Error('useMenu must be used inside MenuProvider')
  return ctx
}
