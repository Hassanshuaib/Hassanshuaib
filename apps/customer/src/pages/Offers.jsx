import { Link } from 'react-router-dom'
import { useMenu } from '../context/MenuContext'
import { Card, SectionTitle } from '../components/UI'

export default function Offers() {
  const { addons } = useMenu()
  const freeAddons = addons.filter((a) => a.kind === 'free')

  return (
    <div className="pop-in pb-4 space-y-6">
      <h1 className="font-display font-extrabold text-2xl text-cream">العروض 🎁</h1>

      <Card>
        <p className="text-3xl mb-2">🛡️</p>
        <SectionTitle>الضمان الذهبي</SectionTitle>
        <p className="text-sm text-cream-soft/75 leading-relaxed">
          ما عجبتك الوجبة؟ حقك محفوظ ونرجّع لك قيمتها، بدون أسئلة. رضاك يهمنا أكثر من أي طلب.
        </p>
      </Card>

      <Card>
        <p className="text-3xl mb-2">⭐</p>
        <SectionTitle>كرت الأختام</SectionTitle>
        <p className="text-sm text-cream-soft/75 leading-relaxed mb-3">
          كل طلب مؤكد يضيف لك ختم. اجمع 8 أختام واحصل على كومبير مجاني بالكامل!
        </p>
        <Link to="/stamps" className="text-orange font-bold text-sm">
          شوف كرتي ←
        </Link>
      </Card>

      <Card>
        <p className="text-3xl mb-2">🥔</p>
        <SectionTitle>إضافات مجانية بلا حدود</SectionTitle>
        <p className="text-sm text-cream-soft/75 leading-relaxed mb-3">
          ركّب كومبيرك بأي عدد من هذي الإضافات مجاناً:
        </p>
        <div className="flex flex-wrap gap-2">
          {freeAddons.map((a) => (
            <span key={a.id} className="text-xs font-semibold bg-navy-700 text-cream-soft/80 px-3 py-1.5 rounded-full">
              {a.name}
            </span>
          ))}
        </div>
      </Card>
    </div>
  )
}
