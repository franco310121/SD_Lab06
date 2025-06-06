package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import org.springframework.boot.CommandLineRunner;

@SpringBootApplication
public class DemoApplication implements CommandLineRunner {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
		try {
			Server server = ServerBuilder.forPort(9091)
					.addService(new CurrencyConverterServiceImpl())
					.build()
					.start();

			System.out.println("Servidor gRPC iniciado en el puerto 9091...");
			server.awaitTermination();
		} catch (Exception e) {
			System.err.println("Error al iniciar el servidor gRPC: " + e.getMessage());
		}
	}
}
