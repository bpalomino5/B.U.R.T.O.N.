package com.burton;

import android.app.Application;

import com.facebook.react.ReactApplication;
import com.wenkesj.voice.VoicePackage;
import net.no_mad.tts.TextToSpeechPackage;
import com.facebook.react.ReactPackage;

import com.reactnativenavigation.NavigationApplication;


import java.util.Arrays;
import java.util.List;

public class MainApplication extends NavigationApplication {

  @Override
   public boolean isDebug() {
       // Make sure you are using BuildConfig from your own application
       return BuildConfig.DEBUG;
   }

  @Override
  protected List<ReactPackage> getPackages() {
    return Arrays.<ReactPackage>asList(
          new VoicePackage(),
          new TextToSpeechPackage()
    );
  }

  @Override
   public List<ReactPackage> createAdditionalReactPackages() {
       return getPackages();
   }


 @Override
  public String getJSMainModuleName() {
      return "index";
  }
}
