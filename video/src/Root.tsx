import { Composition } from "remotion";
import { DropshippingRDC } from "./Video";
import { DropshippingRDC12 } from "./Video12";
import { SansStockRisque } from "./risque/Video";
import { TOTAL_FRAMES as RISQUE_FRAMES } from "./risque/timing";
import { TOTAL12_FRAMES } from "./scenes12";
import { FPS, TOTAL_FRAMES } from "./timing";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="DropshippingRDC"
      component={DropshippingRDC}
      durationInFrames={TOTAL_FRAMES}
      fps={FPS}
      width={1080}
      height={1920}
    />
    {/* Version storyboard en 12 scènes (images du dossier Drive « Identité Claude ») */}
    <Composition
      id="DropshippingRDC12"
      component={DropshippingRDC12}
      durationInFrames={TOTAL12_FRAMES}
      fps={FPS}
      width={1080}
      height={1920}
    />
    {/* « Sans stock ≠ sans risque » : risques et marge réelle du dropshipping en RDC */}
    <Composition
      id="SansStockRisque"
      component={SansStockRisque}
      durationInFrames={RISQUE_FRAMES}
      fps={FPS}
      width={1080}
      height={1920}
    />
  </>
);
