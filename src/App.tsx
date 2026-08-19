/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import MoltenMetal from './components/MoltenMetal';

export default function App() {
  return (
    <MoltenMetal
      color1="#5227FF"
      color2="#3360c1"
      color3="#FFFFFF"
      speed={0.35}
      scale={4}
      detail={3}
      glow={1.6}
      coreSize={0.1}
      swirl={1}
      fold={-0.2}
      blackPoint={0.05}
      brightness={1.3}
      colorMode="molten"
      grain={true}
      grainIntensity={0.05}
      mouseInteraction={true}
      mouseStrength={0.3}
      opacity={1.0}
    />
  );
}
