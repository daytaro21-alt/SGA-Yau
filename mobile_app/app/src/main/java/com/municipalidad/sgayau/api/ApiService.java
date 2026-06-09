package com.municipalidad.sgayau.api;

import com.municipalidad.sgayau.models.Tramite;
import java.util.List;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

public interface ApiService {
    /**
     * Consulta los trámites registrados de un ciudadano específico.
     * Mapea al endpoint GET /tramites/{id_ciudadano} del backend.
     */
    @GET("tramites/{id_ciudadano}")
    Call<List<Tramite>> getTramitesByCiudadano(@Path("id_ciudadano") int idCiudadano);
}
