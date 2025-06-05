FROM openjdk:17-slim

WORKDIR /app

COPY target/demo-0.0.1-SNAPSHOT.jar /app/demo.jar

EXPOSE 3000

CMD ["java", "-jar", "/app/demo.jar"]