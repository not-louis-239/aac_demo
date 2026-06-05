# AAC

**A human voice should never be locked behind a $8,000 paywall.**

**Version**: 0.3.0

This is an open-source, lightweight AAC (Augmentative and Alternative Communication) desktop application written in Python using Pygame and Pyttsx3, relying on highly customiseable JSON configurations, licensed under the GNU General Public License, version 3 (GPLv3 or later). 

## But Why?

Traditional AAC companies charge upwards of $7,000-8,000 for "rugged" devices. Strip away the corporate advertising and these are nothing more than off-the-shelf consumer tablets wrapped in thick plastic with big speakers. The price is artificially inflated only because these companies operate in the realm of medical insurance. If you have government funding, like the NDIS (National Disability Insurance Scheme) in Australia, you wait months for approval. **If you don't have funding, your family is priced out of communication.**

I have a sister who uses an AAC talker device. This project started because I took one look at the price, said "that's outrageous", and realised that a Python interpreter and a dream can outdo decades of corporate monopoly.

The modern human species, *Homo sapiens* has been around for 200,000 years. Social communication is literally baked into our biology. It is what allowed us to share technologies, tell stories, and build communities. And today, communication is more important than ever before, in our ever-more-connected world. A speech or language impairment does not take away from a human being their need to communicate with others. The fact that a modern human voice can be locked behind an $8,000 paywall is an unacceptable tragedy. This project exists to restore the power of speech to those of which it has been deprived for too long.

Even beyond the communication devices themselves, commercial AAC apps trap you into using proprietary symbol sets (like SymbolStix or Tobii Dynavox) that carry heavy licensing fees and strict distribution restrictions. 

To ensure this project stays completely free and safe from corporate DMCA takedowns, **all image icons in this project are hand-drawn and licenced under Creative Commons Attribution-ShareAlike 4.0** (see Licence section for details). No monopolies allowed here.

And it's not just about people with speech disabilities. These proprietary companies took the power away from them. They might come for you next. If proprietary software is allowed to proliferate unchecked, the next generation may inherit a world where they have no rights. So it is the job of our generation to not let that happen, under any circumstance.

## Requirements

- Python 3.x (tested on 3.14.0, older versions may or may not work)
- For further dependencies, run: `pip install -r requirements.txt`

## Licence

This project uses mixed-scope licencing to ensure it stays open-source and free for everyone, while preventing corporate exploitation:
- **Software**: All Python source code and JSON configurations are licensed under the **GNU General Public Licence v3 (GPLv3)** or later. See [LICENCE](./LICENCE) for the GNU GPLv3 licence terms.
- **Icons**: All hand-drawn image icons inside the `assets/images` directory are licenced under the **Creative Commons Attribution-ShareAlike (CC-BY-SA) 4.0**. The licence file can be found inside that directory. See the corresponding [LICENCE](./assets/images/LICENCE) for the licence terms.
- **Fonts**: This project uses fonts licensed under the **SIL Open Font Licence v1.1**. These fonts are available on Google Fonts as follows:
  - Atkinson-Hyperlegible: https://fonts.google.com/specimen/Atkinson+Hyperlegible
  - ComicNeue-Bold: https://fonts.google.com/specimen/Comic+Neue
  - Additionally, a copy of the SIL OFL v1.1 is available at: [LICENCE](./assets/fonts/LICENCE)
