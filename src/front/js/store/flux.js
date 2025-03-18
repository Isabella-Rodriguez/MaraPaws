const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			user: null, // Guardará el usuario autenticado,
            error: null, // Guardará errores en registro/login,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			  // 🟢 REGISTRAR USUARIO
			  registerUser: async (name, last_name, email, password) => {
                try {
                    const response = await fetch("http://127.0.0.1:5000/api/users", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ name, last_name, email, password })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        alert("Registro exitoso");
                        return true;
                    } else {
                        setStore({ error: data.msg });
                        return false;
                    }
                } catch (error) {
                    console.error("Error en el registro:", error);
                    setStore({ error: "Error en el servidor" });
                    return false;
                }
            },

            // 🟠 INICIAR SESIÓN (Por ahora solo verifica credenciales)
            loginUser: async (email, password) => {
                try {
                    const response = await fetch("http://127.0.0.1:5000/api/login", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ email, password })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        setStore({ user: data.user });
                        alert("Inicio de sesión exitoso");
                        return true;
                    } else {
                        setStore({ error: data.msg });
                        return false;
                    }
                } catch (error) {
                    console.error("Error en login:", error);
                    setStore({ error: "Error en el servidor" });
                    return false;
                }
            },

            // 🔴 CERRAR SESIÓN
            logoutUser: () => {
                setStore({ user: null });
                alert("Has cerrado sesión");
            },
			getMessage: async () => {
				try{
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				}catch(error){
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			}
		}
	};
};

export default getState;
