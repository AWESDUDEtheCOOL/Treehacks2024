#include "TFT_eSPI.h"

TFT_eSPI tft;
TFT_eSprite spr = TFT_eSprite(&tft);


void setup() {
  pinMode(WIO_MIC, INPUT);
  tft.begin();
  tft.setRotation(3);
  spr.createSprite(TFT_HEIGHT, TFT_WIDTH);
}

void loop() {
  spr.fillSprite(TFT_BLACK);
  tft.setTextSize(5);
  tft.setTextColor(TFT_RED);

  int val = analogRead(WIO_MIC);
  if (val > 600) {
    tft.drawString("EXPLOSION", 30, 100);
    delay(2000);
  }

  spr.pushSprite(0,0);
  delay(50);
}