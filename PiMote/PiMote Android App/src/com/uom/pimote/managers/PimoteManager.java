package com.uom.pimote.managers;

import android.os.AsyncTask;
import android.util.Log;

import com.uom.pimote.mjpegvideo.MjpegInputStream;
import com.uom.pimote.mjpegvideo.MjpegView;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.IOException;
import java.net.URI;

/**
 * Created by Tom on 02/07/2013.
 */
public class PimoteManager {
    MjpegView mv = null;
    AsyncTask<String, Void, MjpegInputStream> read = null;

    public void onMessage(String[] message){};

    public void startVideo(MjpegView mv, String URL){
        this.mv = mv;
        read = new DoRead().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, URL);
    }

    public void stopVideo() {
        if (mv != null) {
            read.cancel(true);
            mv.stopPlayback();
        }
    }

    public void pauseVideo() {
        if (mv != null) mv.pause();
    }

    public void resumeVideo() {
        if (mv != null) mv.resume();
    }

    public class DoRead extends AsyncTask<String, Void, MjpegInputStream> {
        protected MjpegInputStream doInBackground(String... url) {
            HttpResponse res = null;
            DefaultHttpClient httpclient = new DefaultHttpClient();
            Log.d("MjpegRegular", "1. Sending http request");
            try {
                res = httpclient.execute(new HttpGet(URI.create(url[0])));
                Log.d("MjpegRegular", "2. Request finished, status = " + res.getStatusLine().getStatusCode());
                if (res.getStatusLine().getStatusCode() == 401) {
                    //You must turn off camera User Access Control before this will work
                    return null;
                }
                return new MjpegInputStream(res.getEntity().getContent());
            } catch (ClientProtocolException e) {
                e.printStackTrace();
                Log.d("MjpegRegular", "Request failed-ClientProtocolException", e);
                //Error connecting to camera
            } catch (IOException e) {
                e.printStackTrace();
                Log.d("MjpegRegular", "Request failed-IOException", e);
                //Error connecting to camera
            }

            return null;
        }

        protected void onPostExecute(MjpegInputStream result) {
            mv.setSource(result);
            mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
            mv.showFps(true);
        }
    }

}