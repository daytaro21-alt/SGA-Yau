package com.municipalidad.sgayau.models;

import com.google.gson.annotations.SerializedName;

public class Tramite {
    @SerializedName("id")
    private int id;

    @SerializedName("unique_code")
    private String codigoUnico;

    @SerializedName("title")
    private String titulo;

    @SerializedName("description")
    private String descripcion;

    @SerializedName("procedure_type")
    private String tipoTramite;

    @SerializedName("status_id")
    private int estadoId;

    @SerializedName("suggested_priority")
    private String prioridadSugerida;

    @SerializedName("real_priority")
    private String prioridadReal;

    @SerializedName("prediction_confidence")
    private double confianzaPrediccion;

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getCodigoUnico() {
        return codigoUnico;
    }

    public void setCodigoUnico(String codigoUnico) {
        this.codigoUnico = codigoUnico;
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public String getTipoTramite() {
        return tipoTramite;
    }

    public void setTipoTramite(String tipoTramite) {
        this.tipoTramite = tipoTramite;
    }

    public int getEstadoId() {
        return estadoId;
    }

    public void setEstadoId(int estadoId) {
        this.estadoId = estadoId;
    }

    public String getPrioridadSugerida() {
        return prioridadSugerida;
    }

    public void setPrioridadSugerida(String prioridadSugerida) {
        this.prioridadSugerida = prioridadSugerida;
    }

    public String getPrioridadReal() {
        return prioridadReal;
    }

    public void setPrioridadReal(String prioridadReal) {
        this.prioridadReal = prioridadReal;
    }

    public double getConfianzaPrediccion() {
        return confianzaPrediccion;
    }

    public void setConfianzaPrediccion(double confianzaPrediccion) {
        this.confianzaPrediccion = confianzaPrediccion;
    }
}
