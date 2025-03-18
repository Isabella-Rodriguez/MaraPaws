import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";

export const Register = () => {
    const { actions } = useContext(Context);
    const [formData, setFormData] = useState({ name: "", last_name: "", email: "", password: "" });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const success = await actions.registerUser(formData.name, formData.last_name, formData.email, formData.password);
        if (success) {
            window.location.href = "/login"; // Redirigir tras el registro exitoso
        }
    };

    return (
        <div className="container mt-5">
            <h2>Registro</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="name" placeholder="Nombre" value={formData.name} onChange={handleChange} required />
                <input type="text" name="last_name" placeholder="Apellido" value={formData.last_name} onChange={handleChange} required />
                <input type="email" name="email" placeholder="Correo" value={formData.email} onChange={handleChange} required />
                <input type="password" name="password" placeholder="Contraseña" value={formData.password} onChange={handleChange} required />
                <button type="submit">Registrarse</button>
            </form>
        </div>
    );
};
