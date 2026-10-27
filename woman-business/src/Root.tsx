import { Composition } from "remotion";
import { FPS, TOTAL_FRAMES } from "./timing";
import { WomanBusiness } from "./Video";

export const RemotionRoot: React.FC = () => (
  <Composition id="WomanBusiness" component={WomanBusiness} durationInFrames={TOTAL_FRAMES} fps={FPS} width={1080} height={1920} />
);
