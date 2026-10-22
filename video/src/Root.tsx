import { Composition } from "remotion";
import { DropshippingRDC } from "./Video";
import { FPS, TOTAL_FRAMES } from "./timing";

export const RemotionRoot: React.FC = () => (
  <Composition
    id="DropshippingRDC"
    component={DropshippingRDC}
    durationInFrames={TOTAL_FRAMES}
    fps={FPS}
    width={1080}
    height={1920}
  />
);
