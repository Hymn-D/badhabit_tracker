
document.addEventListener("DOMContentLoaded", () => {
    console.log("Habit Tracker JS Loaded ✅");


    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = "0";
            setTimeout(() => alert.remove(), 600);
        }, 4000);
    });


    const searchInput = document.querySelector("#searchHabits");
    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const filter = this.value.toLowerCase();
            document.querySelectorAll("table tr").forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? "" : "none";
            });
        });
    }


    const reminderElements = document.querySelectorAll("[data-reminder-time]");
    reminderElements.forEach(el => {
        const time = el.getAttribute("data-reminder-time");
        const updateCountdown = () => {
            const now = new Date();
            const [hours, minutes] = time.split(":").map(Number);
            const target = new Date();
            target.setHours(hours, minutes, 0, 0);
            if (target < now) target.setDate(target.getDate() + 1);

            const diff = target - now;
            const hrs = Math.floor(diff / (1000 * 60 * 60));
            const mins = Math.floor((diff / (1000 * 60)) % 60);
            el.textContent = `${hrs}h ${mins}m remaining`;
        };
        updateCountdown();
        setInterval(updateCountdown, 60000);
    });
});
