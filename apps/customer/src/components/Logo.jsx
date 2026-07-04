export default function Logo({ size = 'md' }) {
  const sizes = {
    sm: 'text-xl',
    md: 'text-3xl',
    lg: 'text-5xl',
  }
  return (
    <div className="flex items-center gap-2 select-none">
      <SteamPotato className="w-8 h-8" />
      <span className={`brand-tilt font-display font-extrabold text-cream ${sizes[size]}`}>
        كومبير
      </span>
    </div>
  )
}

export function SteamPotato({ className = 'w-10 h-10' }) {
  return (
    <svg viewBox="0 0 100 100" className={className} fill="none">
      <g className="steam-wisp" style={{ animationDelay: '0s' }}>
        <path d="M35 28 C32 22 38 19 35 12" stroke="#F8E7A0" strokeWidth="3" strokeLinecap="round" opacity="0.8" />
      </g>
      <g className="steam-wisp" style={{ animationDelay: '0.6s' }}>
        <path d="M50 26 C47 20 53 17 50 10" stroke="#F8E7A0" strokeWidth="3" strokeLinecap="round" opacity="0.8" />
      </g>
      <g className="steam-wisp" style={{ animationDelay: '1.1s' }}>
        <path d="M65 28 C62 22 68 19 65 12" stroke="#F8E7A0" strokeWidth="3" strokeLinecap="round" opacity="0.8" />
      </g>
      <path
        d="M20 62 C12 45 25 30 42 27 C58 20 78 28 82 45 C88 60 78 78 60 82 C42 88 26 78 20 62Z"
        fill="#F8E7A0"
        stroke="#E0932F"
        strokeWidth="4"
      />
      <circle cx="42" cy="48" r="3.2" fill="#C97C1F" />
      <circle cx="58" cy="42" r="2.6" fill="#C97C1F" />
      <circle cx="52" cy="62" r="3" fill="#C97C1F" />
      <circle cx="66" cy="60" r="2.4" fill="#C97C1F" />
    </svg>
  )
}
