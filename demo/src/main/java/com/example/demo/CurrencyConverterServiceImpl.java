package com.example.demo;

import com.currency.converter.ConversionRequest;
import com.currency.converter.ConversionResponse;
import com.currency.converter.CurrencyConverterGrpc;
import io.grpc.stub.StreamObserver;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.json.JSONObject;

public class CurrencyConverterServiceImpl extends CurrencyConverterGrpc.CurrencyConverterImplBase {
    private static final String API_KEY = "49fff60613a104e0ac03a2ce";
    private static final String BASE_URL = "https://v6.exchangerate-api.com/v6/" + API_KEY + "/pair/";

    private final OkHttpClient httpClient = new OkHttpClient();

    @Override
    public void convert(ConversionRequest request, StreamObserver<ConversionResponse> responseObserver) {
        String from = request.getSourceCurrency();
        String to = request.getTargetCurrency();
        double amount = request.getAmount();

        try {
            String url = BASE_URL + from + "/" + to;
            Request httpRequest = new Request.Builder().url(url).build();
            Response httpResponse = httpClient.newCall(httpRequest).execute();

            if (!httpResponse.isSuccessful()) {
                throw new RuntimeException("API Error");
            }

            String body = httpResponse.body().string();
            JSONObject json = new JSONObject(body);
            double rate = json.getDouble("conversion_rate");
            double convertedAmount = rate * amount;

            ConversionResponse response = ConversionResponse.newBuilder()
                    .setRate(rate)
                    .setConvertedAmount(convertedAmount)
                    .setMessage("Tipo de cambio de " + from + " a " + to)
                    .build();

            responseObserver.onNext(response);
            responseObserver.onCompleted();

        } catch (Exception e) {
            responseObserver.onError(e);
        }
    }
}
