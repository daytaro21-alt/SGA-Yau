package com.municipalidad.sgayau;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.municipalidad.sgayau.api.ApiClient;
import com.municipalidad.sgayau.models.Tramite;
import java.util.List;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private EditText etCitizenId;
    private Button btnSearch;
    private TextView tvResults;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Enlazar vistas del layout
        etCitizenId = findViewById(R.id.etCitizenId);
        btnSearch = findViewById(R.id.btnSearch);
        tvResults = findViewById(R.id.tvResults);

        btnSearch.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                realizarConsulta();
            }
        });
    }

    private void realizarConsulta() {
        String inputId = etCitizenId.getText().toString().trim();
        if (inputId.isEmpty()) {
            Toast.makeText(this, "Por favor, ingrese el ID del ciudadano.", Toast.LENGTH_SHORT).show();
            return;
        }

        int citizenId;
        try {
            citizenId = Integer.parseInt(inputId);
        } catch (NumberFormatException e) {
            Toast.makeText(this, "El ID debe ser un número entero válido.", Toast.LENGTH_SHORT).show();
            return;
        }

        tvResults.setText("Consultando servidor de SGA-Yau...");

        // Llamada asíncrona mediante Retrofit (no bloquea el Main Thread de Android)
        ApiClient.getApiService().getTramitesByCiudadano(citizenId).enqueue(new Callback<List<Tramite>>() {
            @Override
            public void onResponse(Call<List<Tramite>> call, Response<List<Tramite>> response) {
                // Retrofit maneja esta ejecución directamente en el Main (UI) Thread
                if (response.isSuccessful() && response.body() != null) {
                    List<Tramite> listaTramites = response.body();
                    if (listaTramites.isEmpty()) {
                        tvResults.setText("No se encontraron trámites registrados para el ciudadano ID: " + citizenId);
                    } else {
                        StringBuilder sb = new StringBuilder();
                        sb.append("Trámites encontrados (").append(listaTramites.size()).append("):\n\n");
                        for (Tramite tramite : listaTramites) {
                            sb.append("Código: ").append(tramite.getCodigoUnico()).append("\n");
                            sb.append("Título: ").append(tramite.getTitulo()).append("\n");
                            sb.append("Tipo: ").append(tramite.getTipoTramite()).append("\n");
                            sb.append("Estado (ID): ").append(tramite.getEstadoId()).append("\n");
                            sb.append("Prioridad (ML): ").append(tramite.getPrioridadSugerida() != null ? tramite.getPrioridadSugerida() : "Sin evaluar").append("\n");
                            sb.append("--------------------------------------\n\n");
                        }
                        tvResults.setText(sb.toString());
                    }
                } else {
                    int codigoError = response.code();
                    if (codigoError == 404) {
                        tvResults.setText("Ciudadano con ID " + citizenId + " no está registrado.");
                    } else {
                        tvResults.setText("Error en respuesta del servidor: Código " + codigoError);
                    }
                }
            }

            @Override
            public void onFailure(Call<List<Tramite>> call, Throwable t) {
                // Error de conexión física, servidor apagado o DNS fallido
                tvResults.setText("Error de comunicación:\n" + t.getMessage());
            }
        });
    }
}
