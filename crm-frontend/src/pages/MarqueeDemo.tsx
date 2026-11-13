import MarqueeAlongSvgPath from "@/components/ui/marquee-along-svg-path"

import anchorBolts from "@/assets/products/anchor_bolts.jpg"
import hexBolt from "@/assets/products/hexbolt.jpg"
import nuts from "@/assets/products/nuts.jpg"
import screws from "@/assets/products/screws.jpg"
import threadedRods from "@/assets/products/threaded_rods.jpg"
import washers from "@/assets/products/washers.jpg"

const path =
  "M1 209.434C58.5872 255.935 387.926 325.938 482.583 209.434C600.905 63.8051 525.516 -43.2211 427.332 19.9613C329.149 83.1436 352.902 242.723 515.041 267.302C644.752 286.966 943.56 181.94 995 156.5"

const products = [
  { src: hexBolt, alt: "Stainless steel hex bolts, DIN 933" },
  { src: nuts, alt: "Hex nuts, DIN 934" },
  { src: washers, alt: "Flat washers, DIN 125" },
  { src: screws, alt: "Machine screws, DIN 965" },
  { src: anchorBolts, alt: "Anchor bolts" },
  { src: threadedRods, alt: "Threaded rods" },
]

/**
 * Isolated demo route (/marquee-demo, not linked from nav) for evaluating
 * the marquee-along-svg-path component without touching the live
 * Dashboard or Enquiry Form screens.
 */
export default function MarqueeDemo() {
  return (
    <div className="w-full min-h-[70vh] bg-slate-50 flex items-center justify-center p-8">
      <MarqueeAlongSvgPath
        path={path}
        viewBox="0 0 996 330"
        baseVelocity={8}
        slowdownOnHover={true}
        draggable={true}
        repeat={2}
        dragSensitivity={0.1}
        className="w-full max-w-4xl aspect-[3/1]"
        responsive
        grabCursor
      >
        {products.map((product, i) => (
          <div
            key={i}
            className="w-14 h-full rounded-md overflow-hidden shadow-md hover:scale-150 duration-300 ease-in-out"
          >
            <img
              src={product.src}
              alt={product.alt}
              className="w-full h-full object-cover"
              draggable={false}
            />
          </div>
        ))}
      </MarqueeAlongSvgPath>
    </div>
  )
}
